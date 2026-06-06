# -*- coding: utf-8 -*-

import os

# 解决 Windows + conda + torch + matplotlib 可能出现的 OpenMP 冲突
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# 必须放在 torchvision 前面，避免你当前环境中的 PIL DLL 导入顺序问题
from PIL import Image

import argparse
import random
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SCRIPT_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = SCRIPT_DIR.parent
DEFAULT_DATA_ROOT = CHAPTER_DIR / "cats_and_dogs_filtered"
DEFAULT_PICTURE_DIR = CHAPTER_DIR / "picture"
DEFAULT_MODEL_PATH = CHAPTER_DIR / "best_vgg16_cats_dogs.pth"


RESET = "\033[0m"
GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def color_text(text, color, enable_color=True):
    if not enable_color:
        return text

    return f"{color}{text}{RESET}"


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def format_seconds(seconds):
    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds}s"

    minutes = seconds // 60
    seconds = seconds % 60

    if minutes < 60:
        return f"{minutes}m{seconds}s"

    hours = minutes // 60
    minutes = minutes % 60

    return f"{hours}h{minutes}m{seconds}s"


def print_progress(
    prefix,
    current,
    total,
    loss,
    acc,
    start_time,
    width=32,
    enable_color=True
):
    percent = current / total if total > 0 else 0.0

    filled = int(width * percent)
    if filled >= width:
        done_len = width
        pointer = ""
        left_len = 0
    else:
        done_len = filled
        pointer = "╺"
        left_len = width - done_len - 1

    done_bar = "━" * done_len
    left_bar = "━" * left_len

    done_bar = color_text(done_bar, GREEN, enable_color)
    pointer = color_text(pointer, YELLOW, enable_color)
    left_bar = color_text(left_bar, GRAY, enable_color)

    elapsed = time.time() - start_time
    avg_time = elapsed / current if current > 0 else 0.0
    remain = avg_time * (total - current)

    prefix_text = color_text(prefix, CYAN, enable_color)
    percent_text = color_text(f"{percent * 100:6.2f}%", YELLOW, enable_color)
    loss_text = color_text(f"loss={loss:.4f}", WHITE, enable_color)
    acc_text = color_text(f"acc={acc:.4f}", GREEN, enable_color)

    message = (
        f"\r{prefix_text} "
        f"{done_bar}{pointer}{left_bar} "
        f"{current}/{total} "
        f"{percent_text} "
        f"{loss_text} "
        f"{acc_text} "
        f"elapsed={format_seconds(elapsed)} "
        f"eta={format_seconds(remain)}"
    )

    sys.stdout.write(message)
    sys.stdout.flush()

    if current >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()


def find_dataset_root(data_root):
    root = Path(data_root).resolve()

    candidates = [
        root,
        root / "cats_and_dogs_filtered",
        root.parent / "cats_and_dogs_filtered",
        CHAPTER_DIR / "cats_and_dogs_filtered",
    ]

    for candidate in candidates:
        train_cats = candidate / "train" / "cats"
        train_dogs = candidate / "train" / "dogs"
        val_cats = candidate / "validation" / "cats"
        val_dogs = candidate / "validation" / "dogs"

        if (
            train_cats.exists()
            and train_dogs.exists()
            and val_cats.exists()
            and val_dogs.exists()
        ):
            return candidate, candidate / "train", candidate / "validation"

    raise FileNotFoundError(
        "没有找到数据集目录。请确认目录结构为：\n"
        "chapter10/cats_and_dogs_filtered/train/cats\n"
        "chapter10/cats_and_dogs_filtered/train/dogs\n"
        "chapter10/cats_and_dogs_filtered/validation/cats\n"
        "chapter10/cats_and_dogs_filtered/validation/dogs"
    )


def count_images(folder):
    folder = Path(folder)
    image_suffixes = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    return sum(
        1 for file_path in folder.rglob("*")
        if file_path.suffix.lower() in image_suffixes
    )


def build_dataloaders(data_root, image_size=128, batch_size=16, num_workers=0):
    dataset_root, train_dir, validation_dir = find_dataset_root(data_root)

    print("数据集根目录：", dataset_root)
    print("训练集目录：", train_dir)
    print("验证集目录：", validation_dir)

    print("训练集 cats 数量：", count_images(train_dir / "cats"))
    print("训练集 dogs 数量：", count_images(train_dir / "dogs"))
    print("验证集 cats 数量：", count_images(validation_dir / "cats"))
    print("验证集 dogs 数量：", count_images(validation_dir / "dogs"))

    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std = [0.229, 0.224, 0.225]

    train_transform = transforms.Compose([
        transforms.Resize((image_size + 32, image_size + 32)),
        transforms.RandomResizedCrop(image_size, scale=(0.80, 1.00)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
    ])

    validation_transform = transforms.Compose([
        transforms.Resize((image_size + 32, image_size + 32)),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
    ])

    train_dataset = datasets.ImageFolder(
        root=train_dir,
        transform=train_transform
    )

    validation_dataset = datasets.ImageFolder(
        root=validation_dir,
        transform=validation_transform
    )

    print("类别映射：", train_dataset.class_to_idx)
    print("一般情况下 cats=0，dogs=1。")

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    validation_loader = DataLoader(
        dataset=validation_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    return train_loader, validation_loader, train_dataset.class_to_idx


def build_model(use_pretrained=True, freeze_features=True):
    pretrained_loaded = False

    if use_pretrained:
        try:
            weights = models.VGG16_Weights.IMAGENET1K_V1
            model = models.vgg16(weights=weights)
            pretrained_loaded = True
            print("已加载 ImageNet 预训练 VGG16。")
        except Exception as error:
            print("加载 ImageNet 预训练权重失败。")
            print("可能原因：第一次运行需要联网下载 VGG16 权重。")
            print("现在改用随机初始化 VGG16。")
            print("错误信息：", error)
            model = models.vgg16(weights=None)
    else:
        model = models.vgg16(weights=None)
        print("未使用 ImageNet 预训练权重。")

    if freeze_features and pretrained_loaded:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

        print("已冻结 VGG16 卷积特征提取层，只训练分类器部分。")
    elif freeze_features and not pretrained_loaded:
        print("当前没有成功加载预训练权重，因此不冻结卷积层。")
        print("原因：冻结随机初始化的卷积层会导致模型几乎学不到有效特征。")
    else:
        print("未冻结 VGG16 卷积层，整个模型都会参与训练。")

    input_features = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(input_features, 1)

    return model


def train_one_epoch(
    model,
    dataloader,
    criterion,
    optimizer,
    device,
    epoch,
    total_epochs,
    max_batches=None,
    enable_color=True
):
    model.train()

    total_batches = len(dataloader)

    if max_batches is not None:
        total_batches = min(total_batches, max_batches)

    if total_batches <= 0:
        raise ValueError("训练 batch 数量必须大于 0。")

    total_loss = 0.0
    total_correct = 0
    total_number = 0
    start_time = time.time()

    for batch_index, (images, labels) in enumerate(dataloader, start=1):
        if max_batches is not None and batch_index > max_batches:
            break

        images = images.to(device)
        labels = labels.float().to(device)

        logits = model(images).squeeze(1)
        loss = criterion(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        with torch.no_grad():
            probabilities = torch.sigmoid(logits)
            predictions = (probabilities >= 0.5).long()

            total_correct += (
                predictions.cpu() == labels.cpu().long()
            ).sum().item()

            total_number += labels.size(0)
            total_loss += loss.item() * labels.size(0)

        average_loss = total_loss / total_number
        accuracy = total_correct / total_number

        print_progress(
            prefix=f"Train Epoch [{epoch}/{total_epochs}]",
            current=batch_index,
            total=total_batches,
            loss=average_loss,
            acc=accuracy,
            start_time=start_time,
            enable_color=enable_color
        )

    average_loss = total_loss / total_number
    accuracy = total_correct / total_number

    return average_loss, accuracy


@torch.no_grad()
def evaluate(
    model,
    dataloader,
    criterion,
    device,
    epoch,
    total_epochs,
    max_batches=None,
    enable_color=True
):
    model.eval()

    total_batches = len(dataloader)

    if max_batches is not None:
        total_batches = min(total_batches, max_batches)

    if total_batches <= 0:
        raise ValueError("验证 batch 数量必须大于 0。")

    total_loss = 0.0
    total_correct = 0
    total_number = 0
    start_time = time.time()

    for batch_index, (images, labels) in enumerate(dataloader, start=1):
        if max_batches is not None and batch_index > max_batches:
            break

        images = images.to(device)
        labels = labels.float().to(device)

        logits = model(images).squeeze(1)
        loss = criterion(logits, labels)

        probabilities = torch.sigmoid(logits)
        predictions = (probabilities >= 0.5).long()

        total_correct += (
            predictions.cpu() == labels.cpu().long()
        ).sum().item()

        total_number += labels.size(0)
        total_loss += loss.item() * labels.size(0)

        average_loss = total_loss / total_number
        accuracy = total_correct / total_number

        print_progress(
            prefix=f"Val   Epoch [{epoch}/{total_epochs}]",
            current=batch_index,
            total=total_batches,
            loss=average_loss,
            acc=accuracy,
            start_time=start_time,
            enable_color=enable_color
        )

    average_loss = total_loss / total_number
    accuracy = total_correct / total_number

    return average_loss, accuracy


def save_training_curves(history, picture_dir):
    picture_dir = Path(picture_dir)
    picture_dir.mkdir(parents=True, exist_ok=True)

    epochs = list(range(1, len(history["train_loss"]) + 1))

    loss_path = picture_dir / "loss_curve.png"
    acc_path = picture_dir / "acc_curve.png"

    plt.figure()
    plt.plot(epochs, history["train_loss"], label="train loss")
    plt.plot(epochs, history["validation_loss"], label="validation loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(loss_path, dpi=200)
    plt.close()

    plt.figure()
    plt.plot(epochs, history["train_accuracy"], label="train accuracy")
    plt.plot(epochs, history["validation_accuracy"], label="validation accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(acc_path, dpi=200)
    plt.close()

    print("损失曲线已保存：", loss_path)
    print("准确率曲线已保存：", acc_path)


def denormalize_image(tensor_image):
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

    image = tensor_image.cpu() * std + mean
    image = torch.clamp(image, 0, 1)

    return image


@torch.no_grad()
def save_sample_predictions(model, dataloader, class_to_idx, device, picture_dir):
    picture_dir = Path(picture_dir)
    picture_dir.mkdir(parents=True, exist_ok=True)

    idx_to_class = {
        index: class_name
        for class_name, index in class_to_idx.items()
    }

    model.eval()

    images, labels = next(iter(dataloader))
    images = images.to(device)

    logits = model(images).squeeze(1)
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= 0.5).long().cpu()

    images = images.cpu()
    labels = labels.cpu()

    show_count = min(8, images.size(0))

    plt.figure(figsize=(12, 6))

    for i in range(show_count):
        image = denormalize_image(images[i])
        image = image.permute(1, 2, 0).numpy()

        true_label = idx_to_class[int(labels[i].item())]
        pred_label = idx_to_class[int(predictions[i].item())]
        prob = probabilities[i].item()

        plt.subplot(2, 4, i + 1)
        plt.imshow(image)
        plt.axis("off")
        plt.title(f"T:{true_label}\nP:{pred_label} {prob:.2f}")

    sample_path = picture_dir / "sample_predictions.png"

    plt.tight_layout()
    plt.savefig(sample_path, dpi=200)
    plt.close()

    print("预测样例图已保存：", sample_path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_root",
        type=str,
        default=str(DEFAULT_DATA_ROOT),
        help="数据集根目录，默认是 chapter10/cats_and_dogs_filtered"
    )

    parser.add_argument(
        "--picture_dir",
        type=str,
        default=str(DEFAULT_PICTURE_DIR),
        help="图片保存目录，默认是 chapter10/picture"
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help="模型保存路径，默认是 chapter10/best_vgg16_cats_dogs.pth"
    )

    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--image_size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--num_workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)

    parser.add_argument(
        "--max_train_batches",
        type=int,
        default=None,
        help="只训练前 N 个 batch，用于 CPU 快速测试。默认 None 表示完整训练集。"
    )

    parser.add_argument(
        "--max_val_batches",
        type=int,
        default=None,
        help="只验证前 N 个 batch，用于 CPU 快速测试。默认 None 表示完整验证集。"
    )

    parser.add_argument(
        "--no_pretrained",
        action="store_true",
        help="不使用 ImageNet 预训练权重"
    )

    parser.add_argument(
        "--unfreeze",
        action="store_true",
        help="不冻结 VGG16 卷积层"
    )

    parser.add_argument(
        "--no_color",
        action="store_true",
        help="关闭终端彩色进度条"
    )

    args = parser.parse_args()

    if args.max_train_batches is not None and args.max_train_batches <= 0:
        raise ValueError("--max_train_batches 必须大于 0")

    if args.max_val_batches is not None and args.max_val_batches <= 0:
        raise ValueError("--max_val_batches 必须大于 0")

    enable_color = not args.no_color

    set_seed(args.seed)

    picture_dir = Path(args.picture_dir)
    picture_dir.mkdir(parents=True, exist_ok=True)

    model_path = Path(args.model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("当前脚本目录：", SCRIPT_DIR)
    print("chapter10 目录：", CHAPTER_DIR)
    print("图片保存目录：", picture_dir)
    print("模型保存路径：", model_path)
    print("当前设备：", device)

    train_loader, validation_loader, class_to_idx = build_dataloaders(
        data_root=args.data_root,
        image_size=args.image_size,
        batch_size=args.batch_size,
        num_workers=args.num_workers
    )

    model = build_model(
        use_pretrained=not args.no_pretrained,
        freeze_features=not args.unfreeze
    )

    model = model.to(device)

    criterion = nn.BCEWithLogitsLoss()

    trainable_parameters = [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad
    ]

    optimizer = torch.optim.Adam(
        trainable_parameters,
        lr=args.lr
    )

    history = {
        "train_loss": [],
        "train_accuracy": [],
        "validation_loss": [],
        "validation_accuracy": []
    }

    best_validation_accuracy = 0.0

    for epoch in range(1, args.epochs + 1):
        train_loss, train_accuracy = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            epoch=epoch,
            total_epochs=args.epochs,
            max_batches=args.max_train_batches,
            enable_color=enable_color
        )

        validation_loss, validation_accuracy = evaluate(
            model=model,
            dataloader=validation_loader,
            criterion=criterion,
            device=device,
            epoch=epoch,
            total_epochs=args.epochs,
            max_batches=args.max_val_batches,
            enable_color=enable_color
        )

        history["train_loss"].append(train_loss)
        history["train_accuracy"].append(train_accuracy)
        history["validation_loss"].append(validation_loss)
        history["validation_accuracy"].append(validation_accuracy)

        print(
            f"Epoch [{epoch:03d}/{args.epochs:03d}] "
            f"train_loss={train_loss:.4f} "
            f"train_acc={train_accuracy:.4f} "
            f"val_loss={validation_loss:.4f} "
            f"val_acc={validation_accuracy:.4f}"
        )

        if validation_accuracy > best_validation_accuracy:
            best_validation_accuracy = validation_accuracy

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_to_idx": class_to_idx,
                    "best_validation_accuracy": best_validation_accuracy,
                    "args": vars(args),
                },
                model_path
            )

            print("当前最优模型已保存：", model_path)

    print("训练完成。")
    print("最佳验证集准确率：", best_validation_accuracy)

    save_training_curves(
        history=history,
        picture_dir=picture_dir
    )

    save_sample_predictions(
        model=model,
        dataloader=validation_loader,
        class_to_idx=class_to_idx,
        device=device,
        picture_dir=picture_dir
    )


if __name__ == "__main__":
    main()