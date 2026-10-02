from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import matplotlib.pyplot as plt
from PIL import Image
import random
import cv2
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc


def raw_img_dir(raw_data_dir: Union[str, Path], category_names: List[str]) -> Dict[str, List[Path]]:
    """Scan raw directory structure and categorize images by freshness label."""
    image_paths: Dict[str, List[Path]] = {'Fresh': [], 'Rotten': []}
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

    for category in category_names:
        category_path = Path(raw_data_dir) / category
        if not category_path.exists():
            continue
        for item_folder in category_path.iterdir():
            if not item_folder.is_dir():
                continue
            for freshness_folder in item_folder.iterdir():
                if not freshness_folder.is_dir():
                    continue
                label = freshness_folder.name.strip().capitalize()
                if label in image_paths:
                    for file_path in freshness_folder.iterdir():
                        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                            image_paths[label].append(file_path)
    return image_paths


def plot_class_distribution(class_counts: Dict[str, int], title: str = "Class Distribution") -> None:
    """Plot bar chart representing class balance."""
    labels = list(class_counts.keys())
    values = list(class_counts.values())
    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=['#2ecc71', '#e74c3c'], edgecolor='black', alpha=0.85)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel("Image Count", fontsize=12)
    plt.xlabel("Class", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def show_random_images(image_paths_dict: Dict[str, List[Path]], num_per_class: int = 5, figsize: Tuple[int, int] = (12, 4)) -> None:
    """Display random samples per class for visual inspection."""
    for cls, paths in image_paths_dict.items():
        if not paths:
            continue
        sample_paths = random.sample(paths, min(num_per_class, len(paths)))
        plt.figure(figsize=figsize)
        for i, img_path in enumerate(sample_paths):
            plt.subplot(1, len(sample_paths), i + 1)
            plt.imshow(Image.open(img_path))
            plt.axis("off")
            plt.title(f"{cls}", fontsize=11)
        plt.suptitle(f"Sample Images: {cls}", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()


def show_image_by_path(path: Union[str, Path]) -> None:
    """Display an individual image from file path."""
    img = Image.open(path)
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.title(str(path), fontsize=10)
    plt.tight_layout()
    plt.show()


def plot_image_sizes(image_paths_dict: Dict[str, List[Path]]) -> None:
    """Analyze image resolution and aspect ratio distributions across dataset."""
    widths, heights = [], []

    for cls, paths in image_paths_dict.items():
        for p in paths:
            try:
                with Image.open(p) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
            except Exception:
                continue

    if not widths:
        return

    plt.figure(figsize=(8, 6))
    plt.scatter(widths, heights, alpha=0.3, edgecolors='none', c='#3498db')
    plt.xlabel("Width (px)", fontsize=12)
    plt.ylabel("Height (px)", fontsize=12)
    plt.title("Image Resolution Distribution", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.hist([w / h for w, h in zip(widths, heights) if h > 0], bins=30, color='#9b59b6', edgecolor='black', alpha=0.75)
    plt.title("Aspect Ratio Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Aspect Ratio (Width / Height)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_color_histogram(img_path: Union[str, Path]) -> None:
    """Plot RGB channel color histogram for produce quality and lighting inspection."""
    img = np.array(Image.open(img_path).convert("RGB"))
    colors = ('r', 'g', 'b')
    plt.figure(figsize=(8, 4))

    for i, col in enumerate(colors):
        plt.hist(img[:, :, i].ravel(), bins=256, color=col, alpha=0.5, label=f'{col.upper()} channel')

    plt.legend()
    plt.title(f"Color Histogram: {Path(img_path).name}", fontsize=13, fontweight='bold')
    plt.xlabel("Pixel Intensity", fontsize=11)
    plt.ylabel("Pixel Count", fontsize=11)
    plt.tight_layout()
    plt.show()


def compute_blur_score(img_path: Union[str, Path]) -> float:
    """Compute sharpness metric via Laplacian variance."""
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.0
    return float(cv2.Laplacian(img, cv2.CV_64F).var())


def plot_blur_distribution(image_paths_dict: Dict[str, List[Path]]) -> None:
    """Plot sharpness distribution across dataset samples."""
    blur_scores = []
    for cls, paths in image_paths_dict.items():
        for p in paths:
            blur_scores.append(compute_blur_score(p))

    plt.figure(figsize=(8, 4))
    plt.hist(blur_scores, bins=40, color='#e67e22', edgecolor='black', alpha=0.75)
    plt.title("Sharpness Score Distribution (Laplacian Variance)", fontsize=13, fontweight='bold')
    plt.xlabel("Sharpness Score (Variance of Laplacian)", fontsize=11)
    plt.ylabel("Sample Count", fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def save_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
    save_path: Union[str, Path]
) -> None:
    """Generate and save publication-grade normalized and raw confusion matrix."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6.5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Count'}
    )
    plt.xlabel("Predicted Label", fontsize=12, fontweight='bold')
    plt.ylabel("True Label", fontsize=12, fontweight='bold')
    plt.title("Confusion Matrix Evaluation", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def save_roc_curve(
    y_true: np.ndarray,
    y_pred_probs: np.ndarray,
    num_classes: int,
    save_path: Union[str, Path],
    class_names: Optional[List[str]] = None
) -> None:
    """Plot and save multi-class or binary ROC curves with AUC metrics."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8.5, 6.5))

    if num_classes == 2:
        fpr, tpr, _ = roc_curve(y_true, y_pred_probs[:, 1])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, color='#2980b9', lw=2, label=f"ROC curve (AUC = {roc_auc:.4f})")
    else:
        for i in range(num_classes):
            fpr, tpr, _ = roc_curve(y_true == i, y_pred_probs[:, i])
            roc_auc = auc(fpr, tpr)
            label_name = class_names[i] if class_names and i < len(class_names) else f"Class {i}"
            plt.plot(fpr, tpr, lw=1.8, label=f"{label_name} (AUC = {roc_auc:.4f})")

    plt.plot([0, 1], [0, 1], 'k--', lw=1.2, alpha=0.7)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=12, fontweight='bold')
    plt.ylabel("True Positive Rate (Sensitivity)", fontsize=12, fontweight='bold')
    plt.title("Receiver Operating Characteristic (ROC)", fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=9, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def save_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
    save_path: Union[str, Path]
) -> None:
    """Compute and persist comprehensive per-class classification metrics."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(report)


def save_error_analysis(
    test_ds: Any,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
    save_path: Union[str, Path],
    n_samples: int = 9
) -> None:
    """Perform visual qualitative error analysis by extracting misclassified samples."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    wrong_idx = np.where(y_true != y_pred)[0]

    if len(wrong_idx) == 0:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(
            0.5, 0.5,
            "No Misclassifications Found\n(100% Accuracy on Test Set)",
            ha="center", va="center", fontsize=14, color="green"
        )
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
        return

    n_display = min(len(wrong_idx), n_samples)
    cols = 3 if n_display >= 3 else n_display
    rows = int(np.ceil(n_display / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes_flat = np.array(axes).reshape(-1)

    for n in range(n_display):
        idx = wrong_idx[n]
        img, _ = test_ds.unbatch().skip(int(idx)).take(1).as_numpy_iterator().__next__()

        # Robust color range scaling: handle float [0, 1] vs int [0, 255]
        if np.max(img) <= 1.0:
            display_img = np.clip(img * 255.0, 0, 255).astype("uint8")
        else:
            display_img = np.clip(img, 0, 255).astype("uint8")

        axes_flat[n].imshow(display_img)
        true_name = class_names[y_true[idx]]
        pred_name = class_names[y_pred[idx]]
        axes_flat[n].set_title(f"True: {true_name}\nPred: {pred_name}", fontsize=10, color='red')
        axes_flat[n].axis("off")

    # Disable remaining empty subplots
    for n in range(n_display, len(axes_flat)):
        axes_flat[n].axis("off")

    plt.suptitle("Qualitative Error Analysis (Misclassified Test Samples)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def save_optimization_comparison(results_dict: Dict[str, Any], save_path: Union[str, Path]) -> None:
    """Save model benchmark and evaluation metrics table to CSV."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results_dict)
    df.to_csv(save_path, index=False)

