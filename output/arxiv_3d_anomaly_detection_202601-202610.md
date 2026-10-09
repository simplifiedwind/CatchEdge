# arXiv 科研趋势快照

- 查询关键词：`3d anomaly detection`
- 时间范围：2026-01 ~ 2026-10
- 分类：不限
- 抓取时间：2026-10-09 17:06
- 论文总数：78
- 状态分布：Accepted 16 篇 / Under review 2 篇 / 其他 60 篇

---

## 给分析 agent 的指令

> 请你阅读下面这份论文快照，完成以下任务：
> 1. 按「研究子方向」对论文聚类，给出每个子方向的核心创新点；
> 2. 标出哪些创新点已经被 Accepted 论文占据（= 已被抢先）；
> 3. 指出在 Under review 论文中，哪些方向竞争最激烈；
> 4. 给出 2-3 个「目前还空着、值得下注」的方向。
> 5. 对于 Under review 的论文，请特别注意它们的创新点是否与 Accepted 论文高度重叠——这类意味着窗口期已基本关闭。


---

## ✅ 已接收（Accepted）— 创新点已定局

### 1. Towards Generalizable 3D Anomaly Detection via Relational Inconsistency Modeling

- **arXiv**: [2609.35059v1](http://arxiv.org/abs/2609.35059v1)
- **提交日期**: 2026-09-28
- **分类**: cs.CV
- **Comment**: Accepted by NeurIPS 2026. Code: https://github.com/VisualScienceLab-KHU/GRIM
- **摘要**: 3D anomaly detection (3DAD) aims to identify defective regions in point cloud data, serving as a critical component in industrial inspection systems. Existing methods are normality-centered -- learning the distribution of normal samples and treating deviations as anomalies -- without explicitly modeling what constitutes a defect. This leads to ambiguous decision boundaries with increased false positives and negatives, particularly in unified and cross-domain settings where diverse normal distributions further blur the boundaries. We propose a relational inconsistency modeling framework that characterizes defects as violations of geometric consistency among neighboring structures. Our approach learns category-agnostic defect cues through pseudo-anomalies designed as controlled relational violations, instantiated by two key modules: Edge-aware Graph Refinement (EGR) for encoding geometric relationships among local regions, and Cluster-Deviation Modeling (CDM) for identifying regions that are relationally incompatible within their structural peer group. Extensive experiments on Anomaly-ShapeNet and Real3D-AD demonstrate consistent improvements over prior state-of-the-art methods in both in-domain and cross-domain settings, validating the effectiveness of learning an explicit, relation-based defect criterion for 3D anomaly detection. Project page: https://visualsciencelab-khu.github.io/GRIM_project/.
- **核心创新**（待 agent 提炼）: 

### 2. PADFormer: Pose-agnostic Anomaly Detection from Sparse View Images

- **arXiv**: [2608.04210v1](http://arxiv.org/abs/2608.04210v1)
- **提交日期**: 2026-08-04
- **分类**: cs.CV
- **Comment**: Accepted to ECCV 2026 (oral)
- **摘要**: Pose-agnostic Anomaly Detection (PAD) remains challenging as anomalies can appear under arbitrary viewpoints, requiring methods to handle significant pose variations. Existing approaches rely on complex 3D reconstruction, which are computationally expensive and require extensive multi-view data. We propose PADFormer, a novel image-space approach that leverages Vision Transformer (ViT) to directly reconstruct anomaly-free versions of query images while preserving pose information. Our key insight is to adapt cross-view masked reconstruction for anomaly detection through training exclusively on normal data, combined with dynamic patch selection and spatial alignment mechanisms that enable effective learning from sparse reference views under significant pose variations. During inference, we perform multiple forward passes with different masking patterns to generate an ensemble of anomaly-free reconstructions, ensuring comprehensive coverage of the query image. Anomalies are detected by comparing these reconstructions with the query image. PADFormer achieves state-of-the-art results on the PAD benchmark while maintaining comparable performance on classic few-shot anomaly detection (FSAD) tasks, demonstrating superior efficiency and generalization without requiring 3D reconstruction.
- **核心创新**（待 agent 提炼）: 

### 3. TC-MAF: Train-Calibrated Bounded Multi-Evidence Fusion for Multimodal Industrial Anomaly Detection

- **arXiv**: [2607.11170v1](http://arxiv.org/abs/2607.11170v1)
- **提交日期**: 2026-07-13
- **分类**: cs.CV
- **Comment**: accepted by ACM MM 2026
- **摘要**: Multimodal anomaly detection benefits from complementary RGB and 3D evidence, yet auxiliary RGB reconstruction is not equally reliable across product categories and class-wise test-time policy selection is usually unavailable. We propose TC-MAF, a base-anchored multi-evidence fusion design that combines a multimodal detector, complementary Dinomaly evidence, and a small cross-modal consistency cue under one fixed pixel-level fusion formula. A lightweight training-dispersion confidence (TDC) term scales auxiliary participation using only normal training statistics. On MVTec-3D, TC-MAF reaches 0.979 image-level AUROC and 0.990 pixel-level AUPRO, achieving the best mean results on both detection and localization among the compared multimodal methods. Systematic ablations show that the fusion structure itself is the dominant factor, while TDC provides a smaller but reproducible calibration gain over no calibration or arbitrary calibration. Additional experiments show that the same design remains effective under a pooled-statistics variant, auxiliary-branch and backbone substitutions, few-shot settings, a missing-3D setting, and cross-dataset evaluation on Eyecandies. Code is available at https://anonymous.4open.science/r/TC_MAF-C3BB.
- **核心创新**（待 agent 提炼）: 

### 4. Physics-inspired Pseudo Anomaly Generation and Prototype Feature Guidance for 3D Anomaly Detection

- **arXiv**: [2607.10544v1](http://arxiv.org/abs/2607.10544v1)
- **提交日期**: 2026-07-12
- **分类**: cs.CV
- **Comment**: 20 pages; already accepted by Pattern Recognition
- **摘要**: 3D point cloud anomaly detection plays a vital role in industrial manufacturing, yet it faces significant challenges due to the scarcity and high acquisition cost of real anomalous samples. The inherently anomaly-free training data further hinders detection methods from effectively learning discriminative features between normal and abnormal instances. To address these issues, we propose PA3AD, a novel framework that introduces a physics-inspired pseudo-anomaly generation strategy to create physically plausible anomalous samples from normal data. Additionally, we incorporate prototype features via a weight-sharing mechanism to guide the model in capturing the distribution shifts between normal and anomalous samples. Specifically, PA3AD introduces two key innovations to tackle the scarcity of real anomalies. First, a physics-inspired module generates diverse pseudo-anomalous point clouds from normal data via multi-physics modeling. Second, momentum-updated prototypes and a difference-aware fusion block capture stable normal representations and their discrepancies with pseudo-anomalies. This design effectively learns distribution shifts, achieving superior detection performance. Extensive experiments on the Anomaly-ShapeNet and Real3D-AD datasets demonstrate that our method consistently outperforms existing state-of-the-art approaches. Our code will be made publicly available at https://github.com/NingxiaoJian/PA3AD.
- **核心创新**（待 agent 提炼）: 

### 5. DDStereo: Efficient Dual Decoder Transformers for Stereo 3D Road Anomaly Detection

- **arXiv**: [2606.24805v2](http://arxiv.org/abs/2606.24805v2)
- **提交日期**: 2026-06-23
- **分类**: cs.CV
- **Comment**: Accepted by ECCV2026
- **摘要**: Stereo-based 3D obstacle perception for autonomous driving is currently constrained by an imbalanced triplet: deployment cost, detection accuracy, and open-set adaptability. While existing methods struggle to balance these three competing objectives, there is an urgent demand for high-precision, real-time algorithms capable of detecting arbitrary obstacles in the wild. In this paper, we present DDStereo, a novel Dual-Decoder Stereo Transformer that achieves a synergistic integration of 3D object detection and Out-of-Distribution (OoD) road anomaly detection. Leveraging the geometric priors of stereo disparity, our approach effectively couples 3D attribute regression with open-set foreground detection within a streamlined dual-branch decoder architecture. Conventional methods rely on complex feature-level fusion; DDStereo maintains execution efficiency by employing a decoupled decoding strategy and shared object-level queries to ensure cross-modal target alignment. Extensive evaluations of public benchmarks demonstrate that DDStereo not only achieves state-of-the-art accuracy under open-set and closed-set protocols. Our method delivers real-time performance comparable to monocular 3D detection baselines, providing a cost-effective solution for the perception of obstacles of the normal and OoD category. Code and models are available at https://github.com/shiyi-mu/DDStereo.
- **核心创新**（待 agent 提炼）: 

### 6. CMDS-AD: Cross-Modal Dual-Stream Decoupling for Few-Shot Anomaly Detection

- **arXiv**: [2606.20300v3](http://arxiv.org/abs/2606.20300v3)
- **提交日期**: 2026-06-18
- **分类**: cs.CV
- **Comment**: Accepted to ECCV 2026! Project page: https://cmds-ad.github.io/
- **摘要**: Few-shot anomaly detection remains challenging due to limited training data. Multi-modal anomaly detection (MAD) offers a viable solution, leveraging 3D geometric cues to enrich 2D RGB representations and compensate for this scarcity. However, existing MAD methods apply spatially uniform feature processing, conflating stable macroscopic structures with high-frequency localized defect signals, exacerbating cross-modal misalignment and inflating false-positive rates. To overcome this, we present CMDS-AD, a Cross-Modal Dual-Stream Anomaly Detection framework. A LoRA-guided diffusion model generates diverse RGB samples to mitigate extreme data scarcity. For 3D normal augmentation, we employ a pre-trained diffusion model as a normal estimator. Crucially, this estimator inherently acts as a non-linear low-pass filter, directly extracting low-frequency normal representations from RGB inputs. This establishes an auxiliary estimated stream of purely low-frequency information, anchoring robust structural templates and assisting the uncompressed real stream, containing coupled high- and low-frequency components, to precisely isolate micro-defects. A Coordinate-Aware Hierarchical Feature Mapper adaptively aligns cross-modal semantics, while a multiplicative scoring mechanism filters modality-specific noise. Under the extreme 1-shot setting, CMDS-AD achieves absolute performance gains of 5.7% (I-AUROC) and 2.0% (AUPRO) on MVTec 3D-AD, alongside 7.7% and 5.6% improvements on EyeCandies, establishing a new state-of-the-art. Code is available at https://github.com/Junhaocai27/CMDS-AD
- **核心创新**（待 agent 提炼）: 

### 7. Real-IAD MVN: A Multi-View Normal Vector Dataset and Benchmark for High-Fidelity Industrial Anomaly Detection

- **arXiv**: [2605.07149v1](http://arxiv.org/abs/2605.07149v1)
- **提交日期**: 2026-05-08
- **分类**: cs.CV
- **Comment**: Accepted to CVPR 2025. 15 pages
- **摘要**: Industrial Anomaly Detection (IAD) is critical for quality control, but existing methods struggle with subtle, geometric defects. Standard 2D (RGB) images are sensitive to texture and lighting but often miss fine geometric anomalies. While 3D point clouds capture macro-shape, they are typically too sparse to detect micro-defects like scratches or pits. We address this fundamental data limitation by introducing Real-IAD-MVN (Multi-View Normal), a large-scale industrial dataset. By upgrading our acquisition system, Real-IAD-MVN captures high-fidelity surface normal maps from five distinct viewpoints, replacing sparse 3D data entirely. This provides a comprehensive geometric representation at a micro-detail level, making previously invisible side-wall and occluded defects explicitly detectable. Our experiments, conducted on this new dataset, first provide evidence that incorporating dense, multi-view pseudo-3D (surface normals) yields significantly better detection performance than using sparse 3D point cloud data. To further validate the dataset and provide a strong benchmark, we introduce a baseline method based on reconstruction, which learns to extract cross-modal unified prototypes from the image and normal map streams. We demonstrate that this unified prototype approach surpasses existing state-of-the-art multimodal fusion methods, highlighting the rich potential of our new dataset for advancing geometric anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 8. Two Steps Are All You Need: Efficient 3D Point Cloud Anomaly Detection with Consistency Models

- **arXiv**: [2605.05372v1](http://arxiv.org/abs/2605.05372v1)
- **提交日期**: 2026-05-06
- **分类**: cs.CV
- **Comment**: Accepted to CVPR 2026, at the 9th Workshop on Efficient Deep Learning for Computer Vision (ECV). To be published in the IEEE/CVF CVPR 2026 Workshop Proceedings
- **摘要**: Diffusion models are rapidly redefining 3D anomaly detection in point cloud data. As 3D sensing becomes integral to modern manufacturing, reliable anomaly detection is essential for high-throughput quality assurance and process control. Yet practical deployment on resource-constrained, latency-critical systems remains limited. Existing methods are often computationally prohibitive or unreliable in complex, unmasked regions, and diffusion pipelines are inherently bottlenecked by iterative denoising. In this work, we address this bottleneck by reformulating reconstructionbased anomaly detection through consistency learning, enabling direct prediction of anomaly-free geometry in one or two network evaluations. We further introduce a novel hybrid loss formulation that explicitly enforces reconstruction toward clean data. This design substantially reduces inference cost, achieving up to 80x faster runtime than the current state-of-the-art method, without GPU acceleration, while preserving strong detection performance. It outperforms R3D-AD on Anomaly-ShapeNet with 76.20% I-AUROC and remains competitive on Real3DAD with 72.80% I-AUROC, enabling efficient, low-latency anomaly detection on resource-constrained platforms, including drones, smart industrial cameras, and other edge devices.
- **核心创新**（待 agent 提炼）: 

### 9. Modulate-and-Map: Crossmodal Feature Mapping with Cross-View Modulation for 3D Anomaly Detection

- **arXiv**: [2604.02328v1](http://arxiv.org/abs/2604.02328v1)
- **提交日期**: 2026-04-02
- **分类**: cs.CV
- **Comment**: Accepted at CVPR Findings 2026
- **摘要**: We present ModMap, a natively multiview and multimodal framework for 3D anomaly detection and segmentation. Unlike existing methods that process views independently, our method draws inspiration from the crossmodal feature mapping paradigm to learn to map features across both modalities and views, while explicitly modelling view-dependent relationships through feature-wise modulation. We introduce a cross-view training strategy that leverages all possible view combinations, enabling effective anomaly scoring through multiview ensembling and aggregation. To process high-resolution 3D data, we train and publicly release a foundational depth encoder tailored to industrial datasets. Experiments on SiM3D, a recent benchmark that introduces the first multiview and multimodal setup for 3D anomaly detection and segmentation, demonstrate that ModMap attains state-of-the-art performance by surpassing previous methods by wide margins.
- **核心创新**（待 agent 提炼）: 

### 10. ProOOD: Prototype-Guided Out-of-Distribution 3D Occupancy Prediction

- **arXiv**: [2604.01081v1](http://arxiv.org/abs/2604.01081v1)
- **提交日期**: 2026-04-01
- **分类**: cs.CV
- **Comment**: Accepted to CVPR 2026. The source code is publicly available at https://github.com/7uHeng/ProOOD
- **摘要**: 3D semantic occupancy prediction is central to autonomous driving, yet current methods are vulnerable to long-tailed class bias and out-of-distribution (OOD) inputs, often overconfidently assigning anomalies to rare classes. We present ProOOD, a lightweight, plug-and-play method that couples prototype-guided refinement with training-free OOD scoring. ProOOD comprises (i) prototype-guided semantic imputation that fills occluded regions with class-consistent features, (ii) prototype-guided tail mining that strengthens rare-class representations to curb OOD absorption, and (iii) EchoOOD, which fuses local logit coherence with local and global prototype matching to produce reliable voxel-level OOD scores. Extensive experiments on five datasets demonstrate that ProOOD achieves state-of-the-art performance on both in-distribution 3D occupancy prediction and OOD detection. On SemanticKITTI, it surpasses baselines by +3.57% mIoU overall and +24.80% tail-class mIoU; on VAA-KITTI, it improves AuPRCr by +19.34 points, with consistent gains across benchmarks. These improvements yield more calibrated occupancy estimates and more reliable OOD detection in safety-critical urban driving. The source code is publicly available at https://github.com/7uHeng/ProOOD.
- **核心创新**（待 agent 提炼）: 

### 11. A Semantically Disentangled Unified Model for Multi-category 3D Anomaly Detection

- **arXiv**: [2603.25159v1](http://arxiv.org/abs/2603.25159v1)
- **提交日期**: 2026-03-26
- **分类**: cs.CV
- **Comment**: Accepted by CVPR 2026
- **摘要**: 3D anomaly detection targets the detection and localization of defects in 3D point clouds trained solely on normal data. While a unified model improves scalability by learning across multiple categories, it often suffers from Inter-Category Entanglement (ICE)-where latent features from different categories overlap, causing the model to adopt incorrect semantic priors during reconstruction and ultimately yielding unreliable anomaly scores. To address this issue, we propose the Semantically Disentangled Unified Model for 3D Anomaly Detection, which reconstructs features conditioned on disentangled semantic representations. Our framework consists of three key components: (i) Coarse-to-Fine Global Tokenization for forming instance-level semantic identity, (ii) Category-Conditioned Contrastive Learning for disentangling category semantics, and (iii) a Geometry-Guided Decoder for semantically consistent reconstruction. Extensive experiments on Real3D-AD and Anomaly-ShapeNet demonstrate that our method achieves state-of-the-art for both unified and category-specific models, improving object-level AUROC by 2.8% and 9.1%, respectively, while enhancing the reliability of unified 3D anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 12. Predictive Photometric Uncertainty in Gaussian Splatting for Novel View Synthesis

- **arXiv**: [2603.22786v2](http://arxiv.org/abs/2603.22786v2)
- **提交日期**: 2026-03-24
- **分类**: cs.CV
- **Comment**: Accepted at ECCV26. Project Page: https://chumsy0725.github.io/3DGS-Uncertainty/
- **摘要**: Recent advances in 3D Gaussian Splatting have enabled impressive photorealistic novel view synthesis. However, to transition from a pure rendering engine to a reliable spatial map for autonomous agents and safety-critical applications, knowing where the representation is uncertain is as important as the rendering fidelity itself. We bridge this critical gap by introducing a lightweight, plug-and-play framework for pixel-wise, view-dependent predictive uncertainty estimation. Our post-hoc method formulates uncertainty as a Bayesian-regularized linear least-squares optimization over reconstruction residuals. This architecture-agnostic approach extracts a per-primitive uncertainty channel without modifying the underlying scene representation or degrading baseline visual fidelity. Crucially, we demonstrate that providing this actionable reliability signal successfully translates 3D Gaussian splatting into a trustworthy spatial map, further improving state-of-the-art performance across three critical downstream perception tasks: active view selection, pose-agnostic scene change detection, and pose-agnostic anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 13. Multimodal Industrial Anomaly Detection via Geometric Prior

- **arXiv**: [2603.22757v1](http://arxiv.org/abs/2603.22757v1)
- **提交日期**: 2026-03-24
- **分类**: cs.CV
- **Comment**: Accepted for publication in IEEE Transactions on Circuits and Systems for Video Technology (TCSVT)
- **摘要**: The purpose of multimodal industrial anomaly detection is to detect complex geometric shape defects such as subtle surface deformations and irregular contours that are difficult to detect in 2D-based methods. However, current multimodal industrial anomaly detection lacks the effective use of crucial geometric information like surface normal vectors and 3D shape topology, resulting in low detection accuracy. In this paper, we propose a novel Geometric Prior-based Anomaly Detection network (GPAD). Firstly, we propose a point cloud expert model to perform fine-grained geometric feature extraction, employing differential normal vector computation to enhance the geometric details of the extracted features and generate geometric prior. Secondly, we propose a two-stage fusion strategy to efficiently leverage the complementarity of multimodal data as well as the geometric prior inherent in 3D points. We further propose attention fusion and anomaly regions segmentation based on geometric prior, which enhance the model's ability to perceive geometric defects. Extensive experiments show that our multimodal industrial anomaly detection model outperforms the State-of-the-art (SOTA) methods in detection accuracy on both MVTec-3D AD and Eyecandies datasets.
- **核心创新**（待 agent 提炼）: 

### 14. GS-CLIP: Zero-shot 3D Anomaly Detection by Geometry-Aware Prompt and Synergistic View Representation Learning

- **arXiv**: [2602.19206v3](http://arxiv.org/abs/2602.19206v3)
- **提交日期**: 2026-02-22
- **分类**: cs.CV
- **Comment**: Accepted by CVPR 2026
- **摘要**: Zero-shot 3D Anomaly Detection is an emerging task that aims to detect anomalies in a target dataset without any target training data, which is particularly important in scenarios constrained by sample scarcity and data privacy concerns. While current methods adapt CLIP by projecting 3D point clouds into 2D representations, they face challenges. The projection inherently loses some geometric details, and the reliance on a single 2D modality provides an incomplete visual understanding, limiting their ability to detect diverse anomaly types. To address these limitations, we propose the Geometry-Aware Prompt and Synergistic View Representation Learning (GS-CLIP) framework, which enables the model to identify geometric anomalies through a two-stage learning process. In stage 1, we dynamically generate text prompts embedded with 3D geometric priors. These prompts contain global shape context and local defect information distilled by our Geometric Defect Distillation Module (GDDM). In stage 2, we introduce Synergistic View Representation Learning architecture that processes rendered and depth images in parallel. A Synergistic Refinement Module (SRM) subsequently fuses the features of both streams, capitalizing on their complementary strengths. Comprehensive experimental results on four large-scale public datasets show that GS-CLIP achieves superior performance in detection. Code can be available at https://github.com/zhushengxinyue/GS-CLIP.
- **核心创新**（待 agent 提炼）: 

### 15. Training-Free Zero-Shot Anomaly Detection in 3D Brain MRI with 2D Foundation Models

- **arXiv**: [2602.15315v1](http://arxiv.org/abs/2602.15315v1)
- **提交日期**: 2026-02-17
- **分类**: cs.CV
- **Comment**: Accepted for MIDL 2026
- **摘要**: Zero-shot anomaly detection (ZSAD) has gained increasing attention in medical imaging as a way to identify abnormalities without task-specific supervision, but most advances remain limited to 2D datasets. Extending ZSAD to 3D medical images has proven challenging, with existing methods relying on slice-wise features and vision-language models, which fail to capture volumetric structure. In this paper, we introduce a fully training-free framework for ZSAD in 3D brain MRI that constructs localized volumetric tokens by aggregating multi-axis slices processed by 2D foundation models. These 3D patch tokens restore cubic spatial context and integrate directly with distance-based, batch-level anomaly detection pipelines. The framework provides compact 3D representations that are practical to compute on standard GPUs and require no fine-tuning, prompts, or supervision. Our results show that training-free, batch-based ZSAD can be effectively extended from 2D encoders to full 3D MRI volumes, offering a simple and robust approach for volumetric anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 16. Kidney Cancer Detection Using 3D-Based Latent Diffusion Models

- **arXiv**: [2601.05852v1](http://arxiv.org/abs/2601.05852v1)
- **提交日期**: 2026-01-09
- **分类**: cs.CV
- **Comment**: 8 pages, 2 figures. This paper has been accepted at Bildverarbeitung für die Medizin (BVM) 2026
- **摘要**: In this work, we present a novel latent diffusion-based pipeline for 3D kidney anomaly detection on contrast-enhanced abdominal CT. The method combines Denoising Diffusion Probabilistic Models (DDPMs), Denoising Diffusion Implicit Models (DDIMs), and Vector-Quantized Generative Adversarial Networks (VQ-GANs). Unlike prior slice-wise approaches, our method operates directly on an image volume and leverages weak supervision with only case-level pseudo-labels. We benchmark our approach against state-of-the-art supervised segmentation and detection models. This study demonstrates the feasibility and promise of 3D latent diffusion for weakly supervised anomaly detection. While the current results do not yet match supervised baselines, they reveal key directions for improving reconstruction fidelity and lesion localization. Our findings provide an important step toward annotation-efficient, generative modeling of complex abdominal anatomy.
- **核心创新**（待 agent 提炼）: 

## 🟡 审稿中（Under review）— 创新点竞争窗口

### 1. GRC-Net: Global Representation Consistency Network for Unsupervised Multimodal Anomaly Detection

- **arXiv**: [2610.09329v1](http://arxiv.org/abs/2610.09329v1)
- **提交日期**: 2026-10-07
- **分类**: cs.CV
- **Comment**: 5 pages, 3 figures, Under Review
- **摘要**: Automated quality inspection is essential for ensuring product reliability in manufacturing.While image-based methods effectively capture appearance-related defects, these methods are limited in detecting structural and geometric anomalies, motivating multimodal approaches incorporating 3D information. However, existing methods mainly rely on local patch-level representations, which often lead to unstable reconstruction errors even in normal regions. To address this limitation, we propose GRC-Net, which integrates a global-attention MLP to enforce global representation consistency across patch embeddings with a stable reconstruction module to improve reconstruction stability. The proposed method captures holistic contextual information through a global token and suppresses reconstruction noise by minimizing discrepancies between original and predicted embeddings. Experiments on MVTec 3D-AD and Eyecandies demonstrate that GRC-Net consistently outperforms existing methods at both image and pixel levels. Qualitative results further demonstrate reduced reconstruction errors in normal regions and more distinct reconstruction differences between normal and anomalous regions.
- **核心创新**（待 agent 提炼）: 

### 2. Dreaming the Unseen: World Model-regularized Diffusion Policy for Out-of-Distribution Robustness

- **arXiv**: [2603.21017v1](http://arxiv.org/abs/2603.21017v1)
- **提交日期**: 2026-03-22
- **分类**: cs.RO
- **Comment**: Under review
- **摘要**: Diffusion policies excel at visuomotor control but often fail catastrophically under severe out-of-distribution (OOD) disturbances, such as unexpected object displacements or visual corruptions. To address this vulnerability, we introduce the Dream Diffusion Policy (DDP), a framework that deeply integrates a diffusion world model into the policy's training objective via a shared 3D visual encoder. This co-optimization endows the policy with robust state-prediction capabilities. When encountering sudden OOD anomalies during inference, DDP detects the real-imagination discrepancy and actively abandons the corrupted visual stream. Instead, it relies on its internal "imagination" (autoregressively forecasted latent dynamics) to safely bypass the disruption, generating imagined trajectories before smoothly realigning with physical reality. Extensive evaluations demonstrate DDP's exceptional resilience. Notably, DDP achieves a 73.8% OOD success rate on MetaWorld (vs. 23.9% without predictive imagination) and an 83.3% success rate under severe real-world spatial shifts (vs. 3.3% without predictive imagination). Furthermore, as a stress test, DDP maintains a 76.7% real-world success rate even when relying entirely on open-loop imagination post-initialization.
- **核心创新**（待 agent 提炼）: 

## ⚪ 其他

### 1. Beyond Geometry: Benchmarking and Consistency Reasoning for 3D Logical Anomaly Detection

- **arXiv**: [2609.34143v1](http://arxiv.org/abs/2609.34143v1)
- **提交日期**: 2026-09-28
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Existing 3D industrial anomaly detection mainly targets local geometric deviations. In contrast, many industrial anomalies violate object-level design or assembly rules, which we define as 3D logical anomalies. To address these challenges, we introduce the Industrial Logical Anomaly Detection Dataset (ILGAD), the first scalable benchmark dedicated to logical anomalies in industrial point clouds. ILGAD contains 2,774 samples from 15 categories with point-level annotations and covers existence, specification, pose, and assembly-state errors. To detect such 3D logical anomalies, we propose a consistency reasoning framework that assesses whether local geometry, structure coverage, and spatial relations conform to the normal design. The framework detects geometric changes, unsupported expected structures, and abnormal local arrangements. Experiments on ILGAD, Anomaly-ShapeNet, and IEC3D demonstrate superior object-level detection and point-level localization, showing that the framework effectively detects logical anomalies and generalizes to conventional geometric defects.
- **核心创新**（待 agent 提炼）: 

### 2. AT3D-AD: Anomaly Type-Aware 3D Anomaly Detection via Hierarchical Point-Language Alignment

- **arXiv**: [2609.25930v1](http://arxiv.org/abs/2609.25930v1)
- **提交日期**: 2026-09-22
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Detecting and localizing 3D point-cloud defects is essential for industrial inspection. However, existing methods often suffer from imprecise localization due to the lack of anomaly supervision and reliance on single-granularity representations. To address these limitations, we propose Anomaly Type-Aware 3D Anomaly Detection (AT3D-AD), a unified framework for joint detection, localization, and classification. Specifically, we first design the Physics-Driven Parametric Anomaly Synthesis (PDPAS) module employing multiple parametric functions to generate synthetic anomalies, providing explicit anomaly supervision. Then, we propose the Hierarchical Global-Local Anomaly Alignment (HiGLA) module to align global and local representations within the normal and anomalous groups. Finally, we propose the Semantic-Geometric Anomaly Classification (SGAC) module to jointly learn localization and classification, yielding spatially precise and type-discriminative anomaly representations. Extensive experiments establish new state-of-the-art performance on all four benchmarks. AT3D-AD achieves Object/Point AUROC scores of 98.1\%/98.9\% on Anomaly-ShapeNet and 95.0\%/95.2\% on Real3D-AD, while reaching 74.2\% Macro-F1 for anomaly-type recognition on Real3D-AD.
- **核心创新**（待 agent 提炼）: 

### 3. PC$^2$-AD: Point Cloud Upsampling to Safeguard 3D Anomaly Detection with Resolution-constrained Edge Devices

- **arXiv**: [2609.14722v1](http://arxiv.org/abs/2609.14722v1)
- **提交日期**: 2026-09-13
- **分类**: cs.CV
- **Comment**: 17 pages, including 6 pages of supplementary material. Code: https://github.com/gyutong406-commits/PC2-AD
- **摘要**: Low-cost and low-resolution sensors used in edge deployments can produce test point clouds that are substantially sparser than the normal training data. This train-test sampling-resolution gap changes the local geometry available to a 3D anomaly detector. We propose PC$^2$-AD, a point cloud upsampling framework that compensates sparse test inputs before downstream detection. Target Domain Candidate Generation (TCG) adapts a pretrained upsampler to normal training geometry and generates a dense candidate pool. Geometry-Aware Candidate Filtering (GACF) selects candidates according to geometric spacing and spatial coverage. Normality-Preserving Point Compensation (NPPC) refines the selection by comparing candidate normality scores with those of their input anchors. The selected points are combined with the unchanged input points and processed by the existing detector. Experiments with six detectors on two Anomaly-ShapeNet settings and Real3D-AD show improvements in the mean of object-level and point-level AUROC for all six detectors in each Anomaly-ShapeNet setting and four on Real3D-AD. These results support point cloud compensation as an input-level approach to improving 3D anomaly detection under low-resolution sensing conditions. Code is publicly available at https://github.com/gyutong406-commits/PC2-AD.
- **核心创新**（待 agent 提炼）: 

### 4. Object Model Analysis of a Supercomputer with Digital Twin

- **arXiv**: [2609.13571v1](http://arxiv.org/abs/2609.13571v1)
- **提交日期**: 2026-09-11
- **分类**: cs.DC
- **Comment**: —
- **摘要**: Operators and developers need a mental model of both the structure and the live behavior of a large supercomputer, but its physical layout, logical organization, and streams of per-node telemetry are difficult to relate to one another, making it hard to trace a metric or event back to a specific hardware component. We present DAT, an interactive three-dimensional digital analytics twin of a compute cluster built in a real-time game engine, Unreal Engine. DAT expands a compact, parametric description of a supercomputer, a reusable Digital Twin Prototype (DTP), into a navigable Digital Twin Instance (DTI) that mirrors its physical containment hierarchy of racks, chassis, blades, and network links, encoding each node's role and health in its appearance, while a lightweight event-driven simulator animates job and hardware activity over a virtual clock. Our current implementation adds a two-path node-selection mechanism, unifying direct 3D pointing with command-shell queries, that opens an in-world visual-analytics panel beside any selected component showing summary statistics and live, time-varying metrics. We describe this architecture, report qualitative behavior from the working prototype, and outline the path toward driving the panels with recorded telemetry and in-situ anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 5. Non-destructive 3D doping imaging of silicon sensors

- **arXiv**: [2609.08769v1](http://arxiv.org/abs/2609.08769v1)
- **提交日期**: 2026-09-08
- **分类**: physics.ins-det
- **Comment**: —
- **摘要**: Silicon sensors are the foundational detection medium for X-rays and charged particles. While their bulk dopant distribution determines device performance, it is conventionally assumed homogeneous because traditional profiling is destructive, spatially restricted, and insensitive at the relevant concentrations. Here we introduce a non-destructive 3D doping imaging technique that turns the readout electronics of a charge-integrating hybrid pixel detector into a massively parallelized capacitance-voltage profiler. With a few tens of micrometres of 3D resolution over wafer-scale areas at concentrations on the order of $10^{11}$ cm$^{-3}$, we image the bulk doping concentration of operational sensors. Macroscopically, we resolve depth-evolving concentric doping rings; microscopically, we uncover scattered doping anomalies that distort local electric fields. The rings modulate the depletion voltage, while the anomalies disrupt local charge collection, a previously overlooked cause of pixel yield and performance degradation. By bridging manufacturing signatures with microscopic defects, this approach provides a non-destructive framework for sensor characterization and yield optimization.
- **核心创新**（待 agent 提炼）: 

### 6. GeoMAD: Geometry-Aware Multi-View Anomaly Detection via Deformable Fusion and Distributional Alignment

- **arXiv**: [2608.26724v1](http://arxiv.org/abs/2608.26724v1)
- **提交日期**: 2026-08-27
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Multi-view anomaly detection (MvAD) detects defects by exploiting complementary observations from multiple camera viewpoints. The central challenge is to fuse views with sufficient geometric awareness while remaining scalable to multi-class industrial settings. Existing methods typically fall into two extremes: voxel-based fusion provides explicit geometric alignment but requires costly 3D construction and class-specific assumptions, whereas lightweight patch-based fusion is efficient but relies on discrete candidate matching and lacks continuous cross-view correspondence. In this paper, we propose GeoMAD, a unified multi-view, multi-class AD framework that addresses both geometric correspondence deficiency and distributional inconsistency. Our \textit{Cross-view Deformable Fusion Module} (CDFM) learns content-adaptive, view-pair-specific sampling offsets directly on 2D feature maps and arranges them across a multi-scale window pyramid with image-global reference sampling, enabling hierarchical cross-view correspondence without camera calibration, voxel construction, or class-specific 3D supervision. We further introduce \textit{Distributional View Alignment} (DVA), a self-supervised cross-view regularization loss that aligns each view's bottleneck distribution against a per-instance view-centric target, enforcing global consistency without pixel-level correspondence. Together, CDFM and DVA bridge local geometric correspondence and global distributional consistency, providing geometry-aware and distribution-consistent fusion while preserving the efficiency of 2D feature-space learning. Extensive experiments on Real-IAD and MANTA-Tiny show that GeoMAD achieves strong detection and localization performance in unified MvAD.
- **核心创新**（待 agent 提炼）: 

### 7. GuidedFlow: An Attention-Guided Framework for Anomaly Detection in Additive Manufacturing

- **arXiv**: [2608.22789v1](http://arxiv.org/abs/2608.22789v1)
- **提交日期**: 2026-08-24
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Additive Manufacturing (AM) plays a vital role in the ongoing industrial revolution. However, quality control remains crucial and challenging due to printing defects or potential cyber-physical intrusions. Image or video-based anomaly detection is a key effort towards addressing these challenges. Various approaches have been explored in this domain, including reconstruction-based, embedding-based, and flow-based methods. Though normalizing flow-based methods address some of the core challenges of unforeseen defects and generalization while maintaining detection performance, existing approaches struggle with tiny/stringing defects common in 3D printing. In a small-data setting, this poses a limitation in generalization. To address these limitations, we propose \textbf{GuidedFlow}, a novel attention-guided normalizing flow model for anomaly detection and localization. GuidedFlow employs a pre-trained ResNet model, fine-tuned on the domain dataset. An attention-guided spatial and temporal flow framework models the dynamics across multiple scales and frames. A Spatio-Temporal Attention Network (SAN) enables the flow model to prioritize relevant contextual cues from input frames. We evaluate GuidedFlow on our AM3D-AD dataset, consisting of benign and anomalous real 3D printed object images and videos. We also conduct a comparative study using the MVTec-AD industrial image anomaly detection dataset. Experimental results demonstrate that GuidedFlow outperforms most of the state-of-the-art models with enhanced detection accuracy and AUROC.
- **核心创新**（待 agent 提炼）: 

### 8. The 10th AI City Challenge

- **arXiv**: [2608.17044v1](http://arxiv.org/abs/2608.17044v1)
- **提交日期**: 2026-08-17
- **分类**: cs.CV
- **Comment**: Summary of the 10th AI City Challenge Workshop in conjunction with ECCV 2026
- **摘要**: The 10th AI City Challenge, held with ECCV 2026, marks a decade of community benchmarking for intelligent transportation, smart cities, and physical AI. Since its 2017 start with vehicle detection, classification, and tracking, the challenge has grown into a broad benchmark suite for multi-camera perception, multimodal reasoning, synthetic-to-real learning, generative forecasting, and privacy-preserving evaluation. The 2026 edition continued this growth with 325 registered teams, up from 245 in 2025, and participation from 26 countries and regions, up from 15. Its six primary tracks cover multi-camera 3D perception, transportation safety captioning and VQA, traffic anomaly reasoning, text-based person anomaly search, generative traffic video forecasting, and cross-city object detection. Track 3 further includes two out-of-domain leaderboards, submitted as Tracks 7 and 8, for fisheye traffic-violation understanding and pedestrian situated-intent VQA. This paper summarizes the challenge setup, datasets, evaluation protocols, leaderboard results, and workshop papers. Across tracks, successful systems combine foundation models with geometric grounding, retrieval or reranking, synthetic-data design, domain adaptation, and controlled inference.
- **核心创新**（待 agent 提炼）: 

### 9. Unsupervised Anomaly Detection for Image Dataset Quality Assurance in Multi-Center Breast MRI

- **arXiv**: [2608.16725v2](http://arxiv.org/abs/2608.16725v2)
- **提交日期**: 2026-08-17
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Corrupted, inconsistent, or anomalous data silently threatens the safety and reliability of medical AI. Despite growing regulatory recognition of dataset quality assurance (QA) for high-risk medical AI, scalable automated detection remains underdeveloped. We employ unsupervised anomaly detection (AD) and out-of-distribution (OOD) detection as an automated dataset QA mechanism for multi-center dynamic contrast-enhanced breast MRI.   We build a controlled AD benchmark of 17 realistic QA-relevant anomaly types from six public datasets (protocol violations, processing errors, incorrect anatomical regions) and propose a taxonomy of radiological image anomalies based on human visual perception, enabling fine-grained analysis of AD failure modes. The benchmark includes near-, medium-far-, far-OOD samples, as well as in-distribution and external normal data. Four methods are evaluated: a projection-based method extended with a domain-specific feature extractor and a novel positional encoding, a reconstruction-based approach extended to full 3D volumes with an augmented training objective, and two unmodified hybrid OOD detection methods.   Medium-far- and far-OOD samples are detected reliably, whereas near-OOD samples and external normal data from unseen institutions expose method-specific differences. The 3D reconstruction-based approach best balances detection performance (AUROC: 0.936) and generalization to unseen institutions. The projection-based method with positional encoding achieves the highest overall detection performance (AUROC: 0.954). Both hybrid methods exhibit critical failure modes, confirming that methods validated for one modality or anatomy may not generalize without domain-specific adaptation. Implants and mastectomies remain an open challenge for all methods. Our results establish a foundation and practical guidance on scalable unsupervised QA in medical AI pipelines.
- **核心创新**（待 agent 提炼）: 

### 10. Rethinking Auxiliary Modalities in Multimodal Zero-shot Anomaly Detection: From Semantic Fusion to Conditional Modulation

- **arXiv**: [2608.13973v1](http://arxiv.org/abs/2608.13973v1)
- **提交日期**: 2026-08-14
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Recent foundation model-based methods have endowed RGB images with strong zero-shot anomaly detection (ZSAD) through vision-language pretraining. However, RGB observations alone remain limited in perceiving anomalies dominated by geometric deformation, depth variation, or subtle surface changes. Auxiliary modalities can provide complementary structural information, but existing multimodal methods typically fuse them directly into a shared semantic space, which may disturb the text-aligned anomaly semantics established by RGB foundation models and often requires modality-specific architectures. To address this issue, we propose a plug-and-play auxiliary-conditioned enhancement framework for zero-shot anomaly detection. Instead of reconstructing a joint multimodal anomaly semantic space, our framework preserves the original RGB image-text anomaly matching pathway and uses auxiliary observations as conditional signals for RGB feature refinement, allowing auxiliary modalities to seamlessly enhance existing RGB-based zero-shot anomaly detectors. Specifically, a lightweight meta-learning module takes global RGB and auxiliary representations as input and generates sample-adaptive low-rank residual updates to determine how RGB features should be refined. We further construct uncertainty-aware spatial modulation from the initial RGB anomaly response and auxiliary reliability, which determines where local residual updates are strengthened or suppressed. This global-to-local conditional modulation enables selective multimodal enhancement while preserving the original RGB anomaly semantics. Extensive experiments on MVTec 3D-AD and Eyecandies demonstrate that our framework consistently improves multiple popular RGB-based zero-shot anomaly detectors, achieving state-of-the-art performance for multimodal zero-shot anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 11. MVFM-3DAD: Multi-view Flow Matching for 3D Anomaly Detection via Density Proxy Estimation

- **arXiv**: [2608.12148v1](http://arxiv.org/abs/2608.12148v1)
- **提交日期**: 2026-08-12
- **分类**: cs.GR
- **Comment**: ICIG 2026 oral presentation, 13 pages, 3 tables, 4 figures
- **摘要**: In 3D anomaly detection (3DAD), most existing methods rely on Memory bank retrieval or reconstruction. However, memory-based methods are constrained by the coverage of stored normal features, while reconstruction-based methods may learn identity shortcuts that also reconstruct anomalous inputs well. These limitations motivate a density-oriented approach that evaluates whether a test sample follows the learned normal distribution. To this end, we propose MVFM-3DAD, a flow-based framework that reframes 3DAD as density proxy estimation over the normal data distribution. MVFM-3DAD introduces a Bidirectional Geometric Projector (BGP), whose forward process converts irregular point clouds into structured multi-view representations. The Flow-guided Density Proxy Estimator (FDPE) estimates a reference density for each view feature, after which the backward process of BGP maps these multi-view density estimates to their corresponding 3D points. Building on it, anomalous features can be identified by their terminal normality. Unlike conventional flow-based likelihood estimation, our formulation requires neither input reconstruction nor explicit Jacobian evaluation, yielding a simple and efficient anomaly-scoring mechanism. Extensive experiments show that MVFM-3DAD outperforms the strongest competing methods on Real3D-AD and MVTec3D-AD. Code is available at https://github.com/lil-wayne-0319/MV3D-AD
- **核心创新**（待 agent 提炼）: 

### 12. Damage Classification for 3D Point Cloud Data via 3D Data Analysis and Vision Foundation Model-based 2D Projections

- **arXiv**: [2608.08955v1](http://arxiv.org/abs/2608.08955v1)
- **提交日期**: 2026-08-09
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Fine-grained damage classification of 3D point cloud data (PCD) remains a persistent challenge, constrained by high computational demands and limited labeled data. This study examines two methods: 3D PCD-based damage assessment (3PDA) algorithm and 2D projection damage assessment (2PDA) In our 3PDA analysis algorithm, TDA is used to derive compact representations of 3D PCD segmented by pointNet, which are then integrated with anomaly detection algorithms to quantify structural degradation. We show that TDA effectively compresses geometric structure from VFM-segmented components into discriminative feature vectors and that anomaly detection models can reliably distinguish components with varying damage severity using only 3D PCD inputs. In the 2D projection analysis algorithm, we leverage large VFMs for granular damage detection by projecting 3D PCD into 2D views. These projections allow VFM based models to achieve competitive classification performance while requiring only a fraction of the computational cost associated with full 3D data processing. Our results demonstrate that 2D VFM pipelines in 2PDA can perform strongly on fine-grained damage classification tasks, highlighting their viability as lightweight, resource-efficient alternatives to traditional 3PDA architectures. Comparative evaluation shows that the 3PDA attains higher accuracy but only for a narrow subset of object geometries and at substantially higher computational cost due to its reliance on TDA and the scarcity of high-fidelity 3D datasets. In contrast, the 2PDA algorithm yields slightly lower accuracy but offers an order of magnitude reduction in time complexity and generalizes across a far broader range of object categories.
- **核心创新**（待 agent 提炼）: 

### 13. Parcel2Progression: An Anatomy-aware Longitudinal Framework for Alzheimer's Disease Diagnosis

- **arXiv**: [2608.08753v1](http://arxiv.org/abs/2608.08753v1)
- **提交日期**: 2026-08-09
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Alzheimer's disease (AD) progression is a longitudinal process with subtle pathological cues in the early stages. Yet, computational constraints have limited most neuroimaging models to either compromise spatial information or limit the number of longitudinal scans. We aim to overcome this bottleneck and fully leverage high-resolution, variable-length T1w structural MRI (4D sMRI) scan sequences. We introduce Parcel2Progression (P2P), a Longitudinal Transformer Framework which tackles this challenge using an Atlas-guided Parcel Encoder that tokenizes 3D scans into a set of richer anatomically grounded representations. A Longitudinal Transformer then integrates irregular, arbitrary-length longitudinal visits with patient age. This synergy delivers two key advantages: (1) parcel-specific interpretability, and (2) computational tractability for long-term analysis, which scales linearly with the number of scans compared to a naive quadratic 4D ViT cost. P2P outperforms prior works and baselines in both MCI (Mild Cognitive Impairment) to AD conversion prediction and AD vs. CN (Cognitively Normal) classification tasks across ADNI, AIBL, and MIRIAD datasets. Leveraging longitudinal scans boosts performance over single-scan baselines by up to 5% and 7% in balanced accuracy for AD classification and MCI conversion prediction tasks, respectively. Interpretability analysis using parcel saliencies and attention rollouts reveals clinically consistent atrophy patterns in AD and MCI subjects. We also demonstrate the frameworks' reliability in anomaly detection using a synthetic dataset, and test the model's generalizability for other neurodegenerative diseases like Frontotemporal Dementia.
- **核心创新**（待 agent 提炼）: 

### 14. LIBAD: A Multimodal Anomaly Detection Benchmark for Li-Ion Battery Electrode Manufacturing

- **arXiv**: [2608.07958v1](http://arxiv.org/abs/2608.07958v1)
- **提交日期**: 2026-08-08
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Multimodal industrial anomaly detection has largely focused on discrete products using strongly correlated RGB and 3D observations, leaving continuous process manufacturing and weakly correlated sensing modalities underexplored. We introduce LIBAD, the first multimodal anomaly detection benchmark for Li-ion battery electrode manufacturing. Collected from real roll-to-roll production lines, LIBAD provides aligned double-sided visible-light imaging, high-resolution X-ray radiography, and inline-compatible low-resolution X-ray radiography. Electrode patches in LIBAD exhibit highly homogeneous material appearance, while defect evidence can be strong in one modality but weak or absent in another, resulting in pronounced cross-modal anomaly inconsistency. Benchmarks of representative methods under the inline-compatible visible-light and low-resolution X-ray setting exhibit limited transferability and consistently high false-positive rates. We therefore propose DA-Core, a memory-based method that jointly considers feature-space coverage and local density of normal features during coreset selection, allowing compact memory banks to better preserve fine-grained normal variations. With a coreset ratio of 0.05, DA-Core reduces FPR95 from 60.4% to 54.3% compared with standard farthest point sampling. At this ratio, DA-Core also outperforms the best standard coreset result (obtained at 0.20) while reducing inference time by 43.9%. These results suggest that both the data distribution of normal features and the modality relationship itself require explicit consideration when designing anomaly detection methods for process manufacturing.
- **核心创新**（待 agent 提炼）: 

### 15. Understanding and Overcoming Cross-modal Fusion Bias in Multimodal Anomaly Detection From A Fisher Information Perspective

- **arXiv**: [2608.00986v1](http://arxiv.org/abs/2608.00986v1)
- **提交日期**: 2026-08-02
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Current advancements in Multimodal Anomaly Detection (MAD) are largely driven by enhancing multimodal fusion, particularly through the integration of RGB and Depth data for richer anomaly representation. However, less attention was devoted to analyzing the role of cross-modal fusion bias, a well-known challenge in multimodal learning, in MAD. This gap motivates a key question: can we overcome this bias to break the performance bottleneck of current work? In this paper, we first analyze the impact of cross-modal fusion bias in MAD via the Fisher Information Matrix. Then, grounded in these findings, we propose UCFB, a simple yet effective plug-and-play framework designed to mitigate cross-modal fusion bias in MAD. It achieves this by jointly employing Fisher-information-guided dynamic calibration to adjust modality-specific regularization weights and canonical similarity analysis to improve inter-modal interactions. Extensive experiments on the MVTec 3D-AD and Eyecandies datasets demonstrate that UCFB achieves consistent improvements in single-class, multi-class, and few-shot settings.
- **核心创新**（待 agent 提炼）: 

### 16. Explainable Multimodal AI for Adaptive Calibration of Archaeological Sensing Workflows

- **arXiv**: [2608.00074v1](http://arxiv.org/abs/2608.00074v1)
- **提交日期**: 2026-07-29
- **分类**: cs.CV
- **Comment**: —
- **摘要**: This paper presents a multimodal machine-learning framework for calibration monitoring, quality assessment, and adaptive acquisition support in archaeological digitisation workflows. The proposed approach operates across photogrammetric 3D reconstruction, hyperspectral imaging, X-ray fluorescence spectroscopy, and Raman spectroscopy through a unified pipeline combining deterministic quality indicators, statistical feature representations, machine-learning classification, anomaly detection, and explainable artificial intelligence (XAI). Rather than replacing instrument-level calibration, the framework introduces an additional algorithmic layer that evaluates whether acquisitions are statistically consistent, physically plausible, and suitable for downstream multimodal integration. For each sensing modality, acquisitions are represented through structured feature spaces encoding geometric, spectral, spatial, and statistical properties. These representations are used to identify degradation patterns such as reconstruction artefacts, illumination inconsistencies, spectral distortions, detector instability, baseline fluctuations, and low signal-to-noise conditions. Supervised and unsupervised learning methods are combined with XAI techniques to support both automatic discrimination between acceptable and problematic acquisitions and interpretation of the underlying causes of degradation. The framework additionally supports adaptive feedback and resource-aware acquisition strategies by linking feature-space deviations to acquisition-level corrective actions. Experimental results obtained on multimodal archaeological datasets demonstrate that the proposed methodology captures meaningful acquisition variability and enables robust quality assessment across heterogeneous sensing modalities.
- **核心创新**（待 agent 提炼）: 

### 17. RadSight: Towards Perceptually Reliable Multimodal Radiology Image Understanding

- **arXiv**: [2607.22293v1](http://arxiv.org/abs/2607.22293v1)
- **提交日期**: 2026-07-24
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Medical multimodal large language models (MLLMs) are increasingly expected to perform complex image understanding tasks, yet their reliability is often compromised by frequent errors in visual interpretation. To systematically trace these failures, we traverse the hierarchy from high-level clinical tasks down to fundamental visual perception. We therefore introduce Perception-Bench, a large-scale benchmark comprising 1.13 million samples that assesses medical MLLMs across six dimensions: attribute judgment, spatial grounding, spatial understanding, disease prediction, anomaly detection, and report generation, spanning both 2D and 3D radiology images. Our analysis on Perception-Bench reveals that existing MLLMs lack the ability to capture even the most basic lesion attributes, such as location, size, and density. This inability to ground clinical outputs in primary visual evidence reveals that the models' diagnostic unreliability is rooted in a critical but overlooked bottleneck in low-level visual perception. Motivated by this, we propose RadSight, a perception-driven MLLM built upon a dual 2D/3D encoder architecture that preserves native imaging spatial structures. RadSight formulates medical image understanding as a four-stage progressive process: visual-language alignment, fine-grained visual perception, clinical diagnosis, and diagnostic interpretation. The model is trained on an 8.37 million perception-oriented corpus using progressive curriculum learning. On Perception-Bench, RadSight consistently outperforms existing MLLMs across all six evaluation dimensions, with particularly strong gains in spatial grounding and clinical diagnosis. It also achieves consistent improvements on public 2D and 3D medical benchmarks, further demonstrating that robust low-level visual perception is a critical foundation for reliable clinical understanding. Code and model will be publicly available.
- **核心创新**（待 agent 提炼）: 

### 18. M2P-AD: Memory-to-Prototype Learning with Boundary-aware Score Refinement for 3D Anomaly Detection

- **arXiv**: [2607.13499v1](http://arxiv.org/abs/2607.13499v1)
- **提交日期**: 2026-07-15
- **分类**: cs.CV
- **Comment**: 16 pages, 6 figures
- **摘要**: 3D anomaly detection has recently emerged as an important research topic in computer vision. Although existing methods have achieved high performance, excessive anomaly responses in normal regions and false positives near object boundaries remain unresolved challenges. To address these challenges, we propose a novel 3D anomaly detection model, Memory-to-Prototype Anomaly Detection (M2P-AD), which effectively models the distribution of normal features while suppressing excessive anomaly scores in normal regions and false positives near object boundaries. Specifically, we introduce a Memory-to-Prototype (M2P) module that learns representative prototypes from normal feature embeddings to preserve important structural information of objects. In addition, a Boundary extraction (BE) module is integrated to identify object boundaries, and a Boundary-aware score refinement (BSR) strategy is applied to recalibrate anomaly scores by incorporating boundary characteristics. The proposed method is evaluated on Real3D-AD, Anomaly-ShapeNet, and MulSen-AD, achieving state-of-the-art performance. Qualitative results demonstrate that excessive anomaly scores in normal regions are reduced and false positives near object boundaries are suppressed, resulting in more accurate and stable anomaly localization. The results indicate that the proposed approach enables more reliable 3D anomaly detection and provides a robust solution applicable to real-world industrial environments.
- **核心创新**（待 agent 提炼）: 

### 19. Raman spectroscopic signature of Kitaev magnetism and complex spin-lattice coupling in S = 1/2 antiferromagnet SrLaCoNbO$_6$ double perovskite

- **arXiv**: [2607.07630v1](http://arxiv.org/abs/2607.07630v1)
- **提交日期**: 2026-07-08
- **分类**: cond-mat.str-el
- **Comment**: submitted
- **摘要**: We report a detailed analysis of temperature-dependent Raman spectroscopy and Co $K$-edge extended x-ray absorption fine structure (EXAFS) for a pseudospin-$\tilde{S}=1/2$ insulating antiferromagnet SrLaCoNbO$_6$, a B-site--ordered double perovskite hosting Co$^{2+}$ ($3d^7$) ions on an {\it f.c.c.} sublattice. Notably, pronounced anomalies in the phonon frequency, linewidth and spectral weight are observed around 60~K, well above the long-range antiferromagnetic transition at $T_{\rm N} \approx 15$~K. These renormalizations indicate a significant coupling between lattice and spin degrees of freedom, although a purely structural contribution cannot be excluded. Additional modifications of both high- and low-energy Raman modes are detected near 160-180 K, including changes in linewidth and intensity, variations of the Fano asymmetry parameter, and the emergence of an additional low-energy feature. The asymmetric Fano line shape of selected low-energy modes, together with a broad low-energy continuum and quasielastic response, suggests coupling between discrete phonons and fluctuating magnetic excitations. Moreover, the EXAFS analysis reveals correlated changes in bond distances and Debye-Waller factors around the Co ions near 60~K and 160~K, evidencing subtle local structural distortions and possible magnetostrictive effects. The persistence of anomalous lattice dynamics far above $T_{\rm N}$, combined with the excitation-energy--independent continuum, is consistent with fluctuating bond-directional interactions and proximate Kitaev-like correlations.
- **核心创新**（待 agent 提炼）: 

### 20. Anomaly Factory 3D: A Modular Framework for Diverse Pseudo-Anomaly Synthesis in Unsupervised 3D Anomaly Detection

- **arXiv**: [2606.29181v1](http://arxiv.org/abs/2606.29181v1)
- **提交日期**: 2026-06-28
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Detecting and localizing defects in 3D point clouds is challenging because abnormal samples are scarce and diverse, while training is often limited to normal data. We propose Anomaly Factory 3D (AF3AD), a modular framework that synthesizes diverse pseudo-anomalies from normal point clouds to expand the training data for unsupervised 3D anomaly detection methods that rely on pseudo-anomalies. AF3AD uses a center-conditioned parametric deformation model defined in local PCA frames, with kernel-controlled spatial falloff, anisotropy, directional gating, and normal/tangential displacement fields, enabling a broad set of geometric defect presets. We demonstrate its ease-of-use and effectiveness by integrating AF3AD with an offset-prediction detector and a reconstruction-based anomaly detection method, showing that AF3AD transfers across detection paradigms. Experiments on AnomalyShapeNet and Real3D-AD show consistent improvements in object- and point-level detection and localization, supported by ablations on preset groups and robustness under noise. AF3AD is designed as a standalone synthesis tool to facilitate adoption across different 3D anomaly detection paradigms. Code is available at github.com/vpc-ccg/AF3AD.
- **核心创新**（待 agent 提炼）: 

### 21. Learning Topology-Aware Representations via Test-Time Adaptation for Anomaly Segmentation

- **arXiv**: [2606.28268v1](http://arxiv.org/abs/2606.28268v1)
- **提交日期**: 2026-06-26
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Test-time adaptation (TTA) has emerged as a promising paradigm for mitigating distribution shifts in deep models. However, existing TTA approaches for anomaly segmentation remain limited by their reliance on pixel-level heuristics, such as confidence thresholding or entropy minimisation, which fail to preserve structural consistency under noise and texture variation. Moreover, they typically treat anomaly maps as flat intensity fields, ignoring the higher-order spatial relationships that characterise complex defect geometries. We introduce TopoTTA (Topological Test-Time Adaptation), a novel framework that integrates persistent homology, a tool from topological data analysis, into the TTA pipeline to enforce geometric and structural coherence during adaptation. By applying multi-level cubical complex filtration to anomaly score maps, TopoTTA derives robust topological pseudo-labels that guide a lightweight test-time classifier, enhancing segmentation quality without retraining the backbone model. The approach avoids reliance on method-specific raw-score thresholding for mask binarisation, preserves connectivity, and generalises across both 2D and 3D modalities. Extensive experiments across six standard benchmarks (MVTec AD, VisA, Real-IAD, MVTec 3D-AD, AnomalyShapeNet, and MVTec LOCO) demonstrate an average 15% F1 improvement over state-of-the-art unsupervised anomaly detection and segmentation methods, with the largest gains on anomalies exhibiting complex geometric or structural variations. These findings suggest that integrating topological reasoning into test-time adaptation provides a principled route to structure-aware generalisation, bridging the gap between geometric learning and robust adaptation.
- **核心创新**（待 agent 提炼）: 

### 22. Point Cloud Diffusion with Global and Local Reconstruction for Instance-Level 3D Anomaly Detection

- **arXiv**: [2606.25740v1](http://arxiv.org/abs/2606.25740v1)
- **提交日期**: 2026-06-24
- **分类**: cs.CV
- **Comment**: —
- **摘要**: 3D anomaly detection in point clouds is critical for high-precision industrial manufacturing. Reconstruction-based methods have laid a strong foundation by detecting 3D anomalies through comparisons between defective inputs and their reconstructed normal counterparts. However, existing methods still suffer from two challenges: 1) the foreground weak defective regions such as scratches are hard to reconstruct and detect, where the anomaly deviations in normalized point clouds can be as small as $10^{-3}$; 2) the background non-defective regions are prone to get positional bias in reconstruction, which leads to false positives. To address these challenges, we propose \textbf{PCDiff}, a point cloud diffusion framework for instance-level 3D anomaly generation and detection. In the generation phase, an instance-level multi-modal attention is embedded into the generation framework, where anomalies are conditioned with texture gradient, image patch, text and mask. The instance-level condition enables the high-quality generation of weak-defective anomalies. In the detection phase, a joint local-global reconstruction algorithm is introduced to ensure local anomaly restoration and global geometric consistency, which preserves background normal structure while restoring the foreground defect. Extensive experiments demonstrate that the proposed PCDiff significantly outperforms state-of-the-art methods in both 3D anomaly generation fidelity and reconstruction quality, leading to substantial improvements in anomaly detection accuracy.
- **核心创新**（待 agent 提炼）: 

### 23. CoGeoAD: Hierarchical Color-Geometric Fusion with Multi-View Attention for Zero-Shot 3D Anomaly Detection

- **arXiv**: [2606.25273v1](http://arxiv.org/abs/2606.25273v1)
- **提交日期**: 2026-06-24
- **分类**: cs.CV
- **Comment**: ICML 2026
- **摘要**: Zero-shot 3D anomaly detection is essential for industrial quality inspection, where labeled anomaly samples are scarce. Meanwhile, existing methods lack an effective mechanism to fuse complementary 2D color images with 3D geometric structures, limiting their ability to detect both surface and structural defects in a unified framework. To address these issues, we propose CoGeoAD, a unified CLIP-based framework that fuses color and geometric features by constructing pixel-aligned paired multi-view images. The framework introduces a Data-Driven Multi-View Attention (MVA) mechanism to adaptively aggregate 3D features and a Multi-Stage Color-Geometric Fusion (MS-CGF) module to hierarchically integrate multi-level features from both modalities. Extensive experiments on the MVTec3D-AD and Eyecandies benchmarks demonstrate that CoGeoAD achieves state-of-the-art performance, effectively capturing both structural and textural anomalies in complex industrial scenarios. our source code is available at https://github.com/kingdomShu/CoGeoAD.
- **核心创新**（待 agent 提炼）: 

### 24. A UAV-Mounted Sensor Network for Close-Range Inspection of Wind Turbine Rotor Blades

- **arXiv**: [2606.21220v1](http://arxiv.org/abs/2606.21220v1)
- **提交日期**: 2026-06-19
- **分类**: cs.RO
- **Comment**: The Aerial Inspection for Marine Infrastructures (AIMI) workshop
- **摘要**: Inspection of offshore wind turbine rotor blades is critical for predictive maintenance to maximise efficiency and extend operational lifetime. However, it remains a challenging task due to remote locations, large structural dimensions, and the limitations of current UAV-compatible sensor systems. While existing approaches can detect certain types of surface anomalies, reliable classification of defect types often remains a manual and error-prone process.   This paper presents the design of a UAV-mounted multimodal sensor network combining an industrial RGB camera, a passive thermal infrared camera, and an in-house developed 3D scanner. All sensors are co-calibrated into a common coordinate frame, enabling spatial superimposition of geometric, colour, and thermal data. The system is designed to operate at close range, addressing three fundamental sensing challenges: platform motion, large field of view, and millimetre-level measurement accuracy. Preliminary laboratory results demonstrate synchronised multi-sensor acquisition and initial point cloud reconstructions, forming the basis for future airborne inspection trials.
- **核心创新**（待 agent 提炼）: 

### 25. Toward Training-Free Zero-Shot Anomaly Detection in 3D Medical Images: A Batch-Based Approach Using 2D Foundation Models

- **arXiv**: [2606.18749v1](http://arxiv.org/abs/2606.18749v1)
- **提交日期**: 2026-06-17
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Zero-shot anomaly detection (ZSAD) is attractive for medical imaging because clinical systems must handle heterogeneous acquisition protocols, changing patient populations, and pathologies for which annotated training data may be unavailable. Most existing zero-shot anomaly detection methods are designed for 2D images, and their direct extension to 3D medical volumes is limited by the scarcity of large-scale volumetric foundation models or by the difficulty of utilizing volumetric context. We propose CS3F, a training-free batch-based framework for ZSAD in 3D medical images using 2D foundation models. Each volume is decomposed along multiple anatomical axes and encoded slice-wise by a 2D vision transformer. These are then converted into localized volumetric tokens by pooling neighboring slice features. Anomaly scores are obtained from cross-subject mutual similarity: tokens that lack close analogues in other subjects are assigned higher anomaly scores. To reduce the attenuation of focal lesion signals caused by depth pooling, we introduce a coarse-to-fine tokenization strategy that enables fine-resolution volumetric scoring without exhaustive matching. CS3F is evaluated on brain MRI across metastases, glioma, and stroke, as well as validated on lung CT to test generalizability beyond atlas-aligned brain MRI. The results show that frozen 2D foundation models can support anomaly localization in 3D medical images, and that the benefit of fine tokenization depends strongly on lesion contrast and imaging modality.
- **核心创新**（待 agent 提炼）: 

### 26. Automated 3D Kinematic Monitoring for Circadian Activity and Anomaly Detection in Juvenile Fish

- **arXiv**: [2606.14749v1](http://arxiv.org/abs/2606.14749v1)
- **提交日期**: 2026-06-05
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Precision aquaculture faces a "phenotyping bottleneck" in tracking high-resolution behavioral traits, as conventional methods cannot quantify instantaneous three-dimensional (3D) physical exertion. To address this, we present a high-throughput 3D behavioral phenotyping framework integrating deep learning object detection with binocular stereo vision for real-time monitoring of juvenile tilapia in high-density environments. The system automates non-contact body length estimation and reconstructs 3D swimming trajectories from absolute spatial coordinates. By eliminating 2D perspective distortions, this approach precisely quantifies 3D velocity and acceleration, marking the first estimation of true physical swimming speeds in free-roaming juveniles. Results show the framework successfully establishes circadian locomotor baselines, serving as an early warning system for physiological stress and providing an objective metric for fish vitality.
- **核心创新**（待 agent 提炼）: 

### 27. VT-3DAD: Cross-Category 3D Anomaly Detection via Visual-Text Normal Space Alignment

- **arXiv**: [2606.04369v1](http://arxiv.org/abs/2606.04369v1)
- **提交日期**: 2026-06-03
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Few-shot cross-category 3D anomaly detection aims to determine whether an unknown point cloud belongs to a target normal category using only a few normal references. Existing training-based methods usually require category-wise optimization, while recent training-free methods based on multi-view CLIP visual features mainly rely on visual similarity and may be confused by geometrically similar categories. In this paper, we propose VT-3DAD, a training-free framework for cross-category 3D anomaly detection via Visual-Text Normal Space Alignment. Given few-shot normal references and a test point cloud, VT-3DAD first generates realistic multi-view depth maps and extracts view-wise features using a frozen CLIP visual encoder. The visual branch measures reference-test deviation in the multi-view feature space. In parallel, depth-aware and 3D-aware prompts are encoded by the frozen CLIP text encoder to construct textual normal anchors, which provide semantic normality constraints for the target category. The final anomaly score is obtained by fusing visual deviation from normal references and semantic deviation from the textual normal space. Experiments on the ShapeNetPart dataset demonstrate that VT-3DAD achieves state-of-the-art performance. In particular, VT-3DAD improves the one-shot average AUC-ROC from 92.49% to 94.80% compared with the visual-only baseline, while also reducing the average standard deviation from 5.64 to 3.41.
- **核心创新**（待 agent 提炼）: 

### 28. From 3D Perception to Safety Reasoning: A Graph-Based Framework for Real-Time Underground Mine Monitoring

- **arXiv**: [2606.03460v1](http://arxiv.org/abs/2606.03460v1)
- **提交日期**: 2026-06-02
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Underground coal mining requires personnel and heavy equipment to operate within shared, confined, and poorly illuminated spaces where hazards such as equipment proximity violations, structural instabilities, and occluded blind spots are difficult to anticipate. Conventional monitoring systems, including fixed cameras and rule-based proximity alerts, can detect predefined events but lack the 3D scene understanding and contextual memory needed to identify complex or evolving hazards. This paper presents a continuous monitoring framework that converts colourised 3D point clouds into structured and traceable safety reasoning outputs. The framework combines 3D semantic perception, uncertainty-based anomaly detection, rule-based hazard checks, on-device LLM reasoning, and GraphRAG -based memory analysis to identify immediate hazards and interpret longer-term safety patterns. Scene and temporal graphs serve as the explicit knowledge structure, linking perception outputs across reasoning stages. To overcome the scarcity of labeled underground data, real roadway scans, controlled object placement, and high-fidelity longwall simulation were combined to generate diverse hazard scenarios, while self-supervised pretraining improved segmentation from limited annotations. The perception model achieved 92.7% accuracy at 30 FPS with low memory usage. Across 115 hazard scenarios, rule-based checks achieved 57% coverage, increasing to 76% with contextual LLM reasoning and 93% with memory-based reasoning using historical records. Qualitative results show uncertainty-derived anomaly signals support the interpretation of out-of-distribution hazards beyond predefined classes. Overall, graph-based knowledge representation combined with 3D perception and layered safety reasoning provides a practical foundation for intelligent decision support in underground mine monitoring.
- **核心创新**（待 agent 提炼）: 

### 29. Uni-RCM: Unified Reference-guided Cross-modal Mapping for Multi-Class Anomaly Detection

- **arXiv**: [2605.29455v1](http://arxiv.org/abs/2605.29455v1)
- **提交日期**: 2026-05-28
- **分类**: cs.CV
- **Comment**: This work has been submitted IEEE for potential publication
- **摘要**: Multi-modal industrial anomaly detection typically relies on separate models for each product category, fundamentally limiting practical scalability. When shifting to a unified paradigm that handles diverse classes simultaneously, detection accuracy often degrades due to inter-class interference and feature manifold confusion. To overcome these challenges, we propose a Unified Reference guided Cross-modal Mapping framework, named Uni-RCM. At its core, we propose a reference guide block to dynamically filter out category-specific noise by introducing a learnable reference feature, which captures the commonalities across different modalities. Besides, an offline residual quantizer is proposed to characterize the normal distribution by multiple cascaded codebooks. Extensive evaluations on the MVTec-3D AD dataset demonstrate the state-of-the-art performance in the challenging multi-class setting and in terms of image-level detection and pixel-level localization.
- **核心创新**（待 agent 提炼）: 

### 30. Regulating Anatomy-Aware Rewards via Trajectory-Integral Feedback for Volumetric Computed Tomography Analysis

- **arXiv**: [2605.20277v1](http://arxiv.org/abs/2605.20277v1)
- **提交日期**: 2026-05-19
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Medical vision-language models (VLMs) have rapidly advanced as general-purpose multimodal assistants, yet their deployment in 3D Computed Tomography (CT) analysis remains constrained by a persistent mismatch between optimization objectives and clinical rigor. Current Reinforcement Learning (RL) paradigms still rely on lexical proxy signals that induce ``\textit{Evaluation Hallucinations}'', where models optimize linguistic fluency rather than factual clinical correctness, leading to diagnostically critical errors. To bridge this gap, we introduce the \textbf{Clinical Abnormality Benchmarking Substrate (CABS)}, a structured system that decomposes radiology reports into verifiable clinical semantic units. Using CABS, we identify a ``\textit{Mechanistic Divergence}'' in standard RL, where surface-similarity rewards drive policy gradients to bypass medical facts. We therefore propose \textbf{Trajectory-Integral Feedback GRPO (TIF-GRPO)}, a novel framework integrating control-theoretic principles into policy optimization. By formulating clinical reasoning as a pseudo-temporal trajectory for anomaly discovery, TIF-GRPO regulates anatomy-aware rewards via an integral feedback loop that penalizes persistent omissions as cumulative state errors and suppresses hallucinations as excessive control effort. Experiments on 3D CT benchmarks demonstrate that our approach significantly enhances abnormality detection and clinical faithfulness, establishing a new paradigm for fine-grained regulation in medical VLMs. Our project is available at \href{https://github.com/ZJU4HealthCare/TIF-GRPO}{GitHub}.
- **核心创新**（待 agent 提炼）: 

### 31. Parameter Efficient Multi-Class Intelligent Scheduling for Multimodal Online Distributed Industrial Anomaly Detection

- **arXiv**: [2605.23984v1](http://arxiv.org/abs/2605.23984v1)
- **提交日期**: 2026-05-15
- **分类**: cs.LG
- **Comment**: —
- **摘要**: Industrial anomaly detection has attracted significant attention as a fundamental challenge in industrial systems. The rapid advancement of heterogeneous industrial sensors has driven industrial anomaly detection from unimodal to multimodal paradigms. However, existing methods are primarily designed for centralized and offline settings, overlooking the distributed and continuously generated data characteristic of real-world industrial environments. With the advancement of edge intelligence, modern edge devices are increasingly capable of not only data acquisition but also distributed model training, enabling collaborative intelligence across the system. Industrial anomaly detection represents a critical application in this context. Motivated by these challenges, we propose a novel framework termed Multimodal Online Distributed Industrial Anomaly Detection (MODIAD). We first present a comprehensive workflow for MODIAD and then formulate a Multi-class Intelligent Scheduling (MIS) problem to coordinate cross class model updates by balancing data sufficiency and class update frequency. To efficiently solve this problem, we design a Sequential Marginal Gain Greedy (SMG) algorithm that enables effective multi-class training under resource constraints. Furthermore, to improve the computational and communication efficiency during training, we propose an Resource Efficient Class-Wise Low Rank Adaptation (REC-LoRA) strategy, which significantly reduces system overhead while preserving detection performance. Extensive experiments on two representative multimodal industrial anomaly detection datasets, MVTec 3D-AD and Eyecandies demonstrate that the proposed approach achieves superior performance and efficiency under the MODIAD scenario.
- **核心创新**（待 agent 提炼）: 

### 32. Align3D-AD: Cross-Modal Feature Alignment and Dual-Prompt Learning for Zero-shot 3D Anomaly Detection

- **arXiv**: [2605.05850v1](http://arxiv.org/abs/2605.05850v1)
- **提交日期**: 2026-05-07
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Zero-shot 3D anomaly detection aims to identify anomalies without access to training data from target categories. However, existing methods mainly rely on projecting 3D observations into multi-view representations that primarily capture geometric cues rather than realistic visual semantics and process them with vision encoders pretrained on RGB data, leading to a significant domain gap between the encoder and the projected representations. To address this issue, we propose Align3D-AD, a unified two-stage framework that leverages the RGB modality from auxiliary categories as cross-modal guidance for zero-shot 3D anomaly detection. First, we introduce a cross-modal feature alignment paradigm that maps rendering features into the RGB semantic space. Unlike prior works that implicitly rely on pretrained encoders, our method enables direct semantic transfer from RGB observations. A semantic consistency reweighting strategy is further introduced to refine feature alignment by reweighting local regions according to holistic semantic consistency. Second, we propose a modality-aware prompt learning framework with dual-prompt contrastive alignment. By assigning independent prompts to RGB-aligned and rendering features, our method captures complementary semantics across modalities, while the contrastive alignment further enhances prompt representations to improve discriminability. Extensive experiments on MVTec3D-AD, Eyecandies, and Real3D-AD demonstrate that Align3D-AD consistently outperforms existing zero-shot methods under both one-vs-rest and cross-dataset settings, highlighting its generalization capability and robustness. Code and the dataset will be made available once our paper is accepted.
- **核心创新**（待 agent 提炼）: 

### 33. Learning Discriminative Signed Distance Functions from Multi-scale Level-of-detail Features for 3D Anomaly Detection

- **arXiv**: [2605.03437v2](http://arxiv.org/abs/2605.03437v2)
- **提交日期**: 2026-05-05
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Detecting anomalies from 3D point clouds has received increasing attention in the field of computer vision, with some group-based or point-based methods achieving impressive results in recent years. However, learning accurate point-wise representations for 3D anomaly detection faces great challenges due to the large scale and sparsity of point clouds. In this study, a surface-based method is proposed for 3D anomaly detection, which learns a discriminative signed distance function using multi-scale level-of-detail features. We first present a Noisy Points Generation (NPG) module to generate different types of noise, thereby facilitating the learning of discriminative features by exposing abnormal points. Then, we introduce a Multi-scale Level-of-detail Feature (MLF) module to capture multi-scale information from a point cloud, which provides both fine-grained local and coarse-grained global feature information. Finally, we design an Implicit Surface Discrimination (ISD) module that leverages the extracted multi-scale features to learn an implicit surface representation of point clouds, which effectively trains a signed distance function to distinguish between abnormal and normal points. Experimental results demonstrate that the proposed method achieves an average object-level AUROC of 92.1\% and 85.9\% on the Anomaly-ShapeNet and Real3D-AD datasets, outperforming the current best approach by 2.1\% and 3.6\%, respectively. Codes are available at https://anonymous.4open.science/r/DLF-3AD-DA61.
- **核心创新**（待 agent 提炼）: 

### 34. Breaking the Rigid Prior: Towards Articulated 3D Anomaly Detection

- **arXiv**: [2604.26868v1](http://arxiv.org/abs/2604.26868v1)
- **提交日期**: 2026-04-29
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Existing 3D anomaly detection methods are built on a rigid prior: normal geometry is pose-invariant and can be canonicalized through registration or alignment. This prior does not hold for articulated objects with hinge or sliding joints, where valid pose changes induce structured geometric variations that cannot be collapsed to a single canonical template, causing pose-induced deformations to be misidentified as anomalies while true structural defects are obscured. No existing benchmark addresses this challenge. We introduce ArtiAD, the first large-scale benchmark for articulated 3D anomaly detection, comprising 15,229 point clouds across 39 object categories with dense joint-angle variations and six structural anomaly types. Each sample is annotated with its joint configuration and part-level motion labels, enabling explicit disentanglement of pose-induced geometry from structural defects. ArtiAD also provides a seen/unseen articulation split to evaluate both interpolation and extrapolation to novel joint configurations. We propose Shape-Pose-Aware Signed Distance Field (SPA-SDF), a baseline that replaces the rigid prior with a continuous pose-conditioned implicit field, factorized into an articulation-independent structural prior and a Fourier-encoded joint embedding. At inference, the articulation state is recovered by minimizing reconstruction energy, and anomalies are identified as point-wise deviations from the learned manifold. SPA-SDF achieves 0.884 object-level AUROC on seen configurations and 0.874 on unseen configurations, substantially outperforming all rigid-based baselines. Our code and benchmark will be publicly released to facilitate future research.
- **核心创新**（待 agent 提炼）: 

### 35. EXACT: an explainable anomaly-aware vision foundation model for analysis of 3D chest CT

- **arXiv**: [2604.24146v1](http://arxiv.org/abs/2604.24146v1)
- **提交日期**: 2026-04-27
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Chest computed tomography (CT) is central to the detection and management of thoracic disease, yet the growing scale and complexity of volumetric imaging increasingly exceed what can be addressed by scan-level prediction alone. Clinically useful AI for CT must not only recognize disease across the whole volume, but also localize abnormalities and provide interpretable visual evidence. Existing vision-language foundation models typically compress scans and reports into global image-text representations, limiting their ability to preserve spatial evidence and support clinically meaningful interpretation. Here we developed EXACT, an explainable anomaly-aware foundation model for three-dimensional chest CT that learns spatially resolved representations from paired clinical scans and radiology reports. EXACT was pre-trained on 25,692 CT-reports pairs using anatomy-aware weak supervision, jointly learning organ segmentation and multi-instance anomaly localization without manual voxel-level annotations. The resulting organ-specific anomaly-aware maps assign each voxel a disease-specific anomaly score confined to its corresponding anatomy, jointly encoding lesion extent and organ-level context. In retrospective multinational and multi-center evaluations, EXACT showed broad and consistent improvements across clinically relevant CT tasks, spanning multi-disease diagnosis, zero-shot anomaly localization, downstream adaptation, and visually grounded report generation, outperforming existing three-dimensional medical foundation models. By transforming routine clinical CT scans and free-text reports into explainable voxel-level representations, EXACT establishes a scalable paradigm for trustworthy volumetric medical AI.
- **核心创新**（待 agent 提炼）: 

### 36. Text-Guided Multimodal Unified Industrial Anomaly Detection

- **arXiv**: [2604.22899v1](http://arxiv.org/abs/2604.22899v1)
- **提交日期**: 2026-04-24
- **分类**: cs.CV
- **Comment**: 12 pages
- **摘要**: Industrial anomaly detection based on RGB-3D multimodal data has emerged as a mainstream paradigm for intelligent quality inspection. However, existing unsupervised methods suffer from two critical limitations: ambiguous cross-modal alignment caused by the lack of high-level semantic guidance and insufficient geometric modeling for RGB-to-3D feature mapping. To address these issues, we propose a unified multimodal industrial anomaly detection framework guided by text semantics. The framework consists of two core modules: a Geometry-Aware Cross-Modal Mapper to preserve geometric structure during modality conversion, and an Object-Conditioned Textual Feature Adaptor to align multimodal features with semantic priors. Furthermore, we establish a unified learning paradigm for multimodal industrial anomaly detection, which breaks the one-model-one-class constraint and enables accurate anomaly detection across diverse classes using a single model. Extensive experiments on the MVTec 3D-AD and Eyecandies datasets demonstrate that our method achieves state-of-the-art performance in classification and localization under unsupervised settings.
- **核心创新**（待 agent 提炼）: 

### 37. ZSG-IAD: A Multimodal Framework for Zero-Shot Grounded Industrial Anomaly Detection

- **arXiv**: [2604.17949v1](http://arxiv.org/abs/2604.17949v1)
- **提交日期**: 2026-04-20
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Deep learning-based industrial anomaly detectors often behave as black boxes, making it hard to justify decisions with physically meaningful defect evidence. We propose ZSG-IAD, a multimodal vision-language framework for zero-shot grounded industrial anomaly detection. Given RGB images, sensor images, and 3D point clouds, ZSG-IAD generates structured anomaly reports and pixel-level anomaly masks. ZSG-IAD introduces a language-guided two-hop grounding module: (1) anomaly-related sentences select evidence-like latent slots distilled from multimodal features, yielding coarse spatial support; (2) selected slots modulate feature maps via channel-spatial gating and a lightweight decoder to produce fine-grained masks. To improve reliability, we further apply Executable-Rule GRPO with verifiable rewards to promote structured outputs, anomaly-region consistency, and reasoning-conclusion coherence. Experiments across multiple industrial anomaly benchmarks show strong zero-shot performance and more transparent, physically grounded explanations than prior methods. We will release code and annotations to support future research on trustworthy industrial anomaly detection systems.
- **核心创新**（待 agent 提炼）: 

### 38. Synthesis4AD: Synthetic Anomalies are All You Need for 3D Anomaly Detection

- **arXiv**: [2604.04658v1](http://arxiv.org/abs/2604.04658v1)
- **提交日期**: 2026-04-06
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Industrial 3D anomaly detection performance is fundamentally constrained by the scarcity and long-tailed distribution of abnormal samples. To address this challenge, we propose Synthesis4AD, an end-to-end paradigm that leverages large-scale, high-fidelity synthetic anomalies to learn more discriminative representations for 3D anomaly detection. At the core of Synthesis4AD is 3D-DefectStudio, a software platform built upon the controllable synthesis engine MPAS, which injects geometrically realistic defects guided by higher-dimensional support primitives while simultaneously generating accurate point-wise anomaly masks. Furthermore, Synthesis4AD incorporates a multimodal large language model (MLLM) to interpret product design information and automatically translate it into executable anomaly synthesis instructions, enabling scalable and knowledge-driven anomalous data generation. To improve the robustness and generalization of the downstream detector on unstructured point clouds, Synthesis4AD further introduces a training pipeline based on spatial-distribution normalization and geometry-faithful data augmentations, which alleviates the sensitivity of Point Transformer architectures to absolute coordinates and improves feature learning under realistic data variations. Extensive experiments demonstrate state-of-the-art performance on Real3D-AD, MulSen-AD, and a real-world industrial parts dataset. The proposed synthesis method MPAS and the interactive system 3D-DefectStudio will be publicly released at https://github.com/hustCYQ/Synthesis4AD.
- **核心创新**（待 agent 提炼）: 

### 39. Hierarchical Point-Patch Fusion with Adaptive Patch Codebook for 3D Shape Anomaly Detection

- **arXiv**: [2604.03972v1](http://arxiv.org/abs/2604.03972v1)
- **提交日期**: 2026-04-05
- **分类**: cs.CV
- **Comment**: 10 pages, 5 figures, 6 tables
- **摘要**: 3D shape anomaly detection is a crucial task for industrial inspection and geometric analysis. Existing deep learning approaches typically learn representations of normal shapes and identify anomalies via out-of-distribution feature detection or decoder-based reconstruction. They often fail to generalize across diverse anomaly types and scales, such as global geometric errors (e.g., planar shifts, angle misalignments), and are sensitive to noisy or incomplete local points during training. To address these limitations, we propose a hierarchical point-patch anomaly scoring network that jointly models regional part features and local point features for robust anomaly reasoning. An adaptive patchification module integrates self-supervised decomposition to capture complex structural deviations. Beyond evaluations on public benchmarks (Anomaly-ShapeNet and Real3D-AD), we release an industrial test set with real CAD models exhibiting planar, angular, and structural defects. Experiments on public and industrial datasets show superior AUC-ROC and AUC-PR performance, including over 40% point-level improvement on the new industrial anomaly type and average object-level gains of 7% on Real3D-AD and 4% on Anomaly-ShapeNet, demonstrating strong robustness and generalization.
- **核心创新**（待 agent 提炼）: 

### 40. Open-Set Supervised 3D Anomaly Detection: An Industrial Dataset and a Generalisable Framework for Unknown Defects

- **arXiv**: [2604.01171v1](http://arxiv.org/abs/2604.01171v1)
- **提交日期**: 2026-04-01
- **分类**: cs.CV
- **Comment**: Resources: https://github.com/hzzzzzhappy/open-industry
- **摘要**: Although self-supervised 3D anomaly detection assumes that acquiring high-precision point clouds is computationally expensive, in real manufacturing scenarios it is often feasible to collect a limited number of anomalous samples. Therefore, we study open-set supervised 3D anomaly detection, where the model is trained with only normal samples and a small number of known anomalous samples, aiming to identify unknown anomalies at test time. We present Open-Industry, a high-quality industrial dataset containing 15 categories, each with five real anomaly types collected from production lines. We first adapt general open-set anomaly detection methods to accommodate 3D point cloud inputs better. Building upon this, we propose Open3D-AD, a point-cloud-oriented approach that leverages normal samples, simulated anomalies, and partially observed real anomalies to model the probability density distributions of normal and anomalous data. Then, we introduce a simple Correspondence Distributions Subsampling to reduce the overlap between normal and non-normal distributions, enabling stronger dual distributions modeling. Based on these contributions, we establish a comprehensive benchmark and evaluate the proposed method extensively on Open-Industry as well as established datasets including Real3D-AD and Anomaly-ShapeNet. Benchmark results and ablation studies demonstrate the effectiveness of Open3D-AD and further reveal the potential of open-set supervised 3D anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 41. Robust Flat Magnetoresistivity in D0$_3$-Fe$_3$Ga Driven by Chiral Anomaly

- **arXiv**: [2603.29138v1](http://arxiv.org/abs/2603.29138v1)
- **提交日期**: 2026-03-31
- **分类**: cond-mat.mtrl-sci
- **Comment**: main text 18 pages, 4 figures
- **摘要**: Topologically non-trivial nodes emerging from flat-band crossings not only enhance unconventional topological responses but also play a fundamental role in exploring correlation-driven topological physics. Here, we report the exceptionally robust chiral-anomaly-dominated transport in D0_3-Fe_3Ga. First, we observe a combination of positive and negative magnetoresistance, ideal planar longitudinal magnetoresistance (PLMR), and the planar Hall effect (PHE). Second, ultra-low-temperature resistivity exhibits pronounced non-Fermi-liquid (NFL) behavior, accompanied by the emergence of giant intrinsic anomalous Hall conductivity (AHC), in excellent agreement with our DFT calculations, which confirm the existence of tilted Weyl points arising from crossings of nearly three-dimensional (3D) flat bands. Most remarkably, we detect an exceptionally robust flat magnetoresistance (flat-MR) that persists without decay up to 33 T. This set of phenomena provides strong evidence that the Fermi level intersects the flattened Weyl crossings, offering confirmation of a topological flat-band semimetal. D0_3-Fe_3Ga presents a promising magnetic platform for quantum device innovations.
- **核心创新**（待 agent 提炼）: 

### 42. Fast localization of anomalous patches in spatial data under dependence

- **arXiv**: [2603.27546v1](http://arxiv.org/abs/2603.27546v1)
- **提交日期**: 2026-03-29
- **分类**: stat.ME
- **Comment**: —
- **摘要**: We propose a scalable, provably accurate method for localizing an unknown number of multiple axis-aligned anomalous patches in spatial data under a general class of spatial dependence. Motivated by the practical need to detect localized changes rather than completely segment large spatial grids, we first introduce both a naive and a significantly faster intelligent-sampling-based estimator for a single patch. We then extend this methodology to the highly challenging multiple-patch setting and propose a two-stage Spatial Patch Localization of Anomalies under DEpendence procedure (SPLADE). Under mild conditions on signal strength, separation from the boundary, inter-patch separation, and a uniform Gaussian approximation, we establish simultaneous consistency for the estimated number of patches and for each individual patch boundary. Extensive numerical results based on synthetic data scenarios demonstrate that the proposed method exhibits significant computational and accuracy gains over competing approaches, as well as robustness to moderate and severe spatial dependence. Finally, we demonstrate the real-world utility of the proposed method by applying it to frame-to-frame video surveillance data, where it accurately detects small, closely separated subjects, a task where existing methods are significantly slower and highly prone to spurious detections due to not accounting for spatial dependence. A second application on 3D fibrous media is deferred to the Appendix.
- **核心创新**（待 agent 提炼）: 

### 43. Back to Point: Exploring Point-Language Models for Zero-Shot 3D Anomaly Detection

- **arXiv**: [2603.21511v3](http://arxiv.org/abs/2603.21511v3)
- **提交日期**: 2026-03-23
- **分类**: cs.CV
- **Comment**: CVPR 2026
- **摘要**: Zero-shot (ZS) 3D anomaly detection is crucial for reliable industrial inspection, as it enables detecting and localizing defects without requiring any target-category training data. Existing approaches render 3D point clouds into 2D images and leverage pre-trained Vision-Language Models (VLMs) for anomaly detection. However, such strategies inevitably discard geometric details and exhibit limited sensitivity to local anomalies. In this paper, we revisit intrinsic 3D representations and explore the potential of pre-trained Point-Language Models (PLMs) for ZS 3D anomaly detection. We propose BTP (Back To Point), a novel framework that effectively aligns 3D point cloud and textual embeddings. Specifically, BTP aligns multi-granularity patch features with textual representations for localized anomaly detection, while incorporating geometric descriptors to enhance sensitivity to structural anomalies. Furthermore, we introduce a joint representation learning strategy that leverages auxiliary point cloud data to improve robustness and enrich anomaly semantics. Extensive experiments on Real3D-AD and Anomaly-ShapeNet demonstrate that BTP achieves superior performance in ZS 3D anomaly detection. Code will be available at \href{https://github.com/wistful-8029/BTP-3DAD}{https://github.com/wistful-8029/BTP-3DAD}.
- **核心创新**（待 agent 提炼）: 

### 44. HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation

- **arXiv**: [2603.12696v2](http://arxiv.org/abs/2603.12696v2)
- **提交日期**: 2026-03-13
- **分类**: cs.RO
- **Comment**: —
- **摘要**: Vision-and-Language Navigation (VLN) is shifting from rigid, step-by-step instruction following toward open-vocabulary, goal-oriented autonomy. Achieving this transition without exhaustive routing prompts requires agents to leverage structural priors. While prior work often assumes computationally heavy 2D/3D metric maps, we instead exploit a lightweight, text-based osmAG (OpenStreetMap Area Graph), a floorplan-level topological representation that is easy to obtain and maintain. However, global planning over a prior map alone is brittle in real-world deployments, where local connectivity can change (e.g., closed doors or crowded passages), leading to execution-time failures. To address this gap, we propose a hierarchical navigation framework HaltNav that couples the robust global planning of osmAG with the local exploration and instruction-grounding capability of VLN. Our approach features an MLLM-based brain module, which is capable of high-level task grounding and obstruction awareness. Conditioned on osmAG, the brain converts the global route into a sequence of localized execution snippets, providing the VLN executor with prior-grounded, goal-centric sub-instructions. Meanwhile, it detects local anomalies via a mechanism we term Reactive Visual Halting (RVH), which interrupts the local control loop, updates osmAG by invalidating the corresponding topology, and triggers replanning to orchestrate a viable detour. To train this halting capability efficiently, we introduce a data synthesis pipeline that leverages generative models to inject realistic obstacles into otherwise navigable scenes, substantially enriching hard negative samples. Extensive experiments demonstrate that our hierarchical framework outperforms several baseline methods without tedious language instructions, and significantly improves robustness for long-horizon vision-language navigation under environmental changes.
- **核心创新**（待 agent 提炼）: 

### 45. Beam-Plasma Collective Oscillations in Intense Charged-Particle Beams: Dielectric Response Theory, Langmuir Wave Dispersion, and Unsupervised Detection via Prometheus

- **arXiv**: [2603.10457v4](http://arxiv.org/abs/2603.10457v4)
- **提交日期**: 2026-03-11
- **分类**: physics.plasm-ph
- **Comment**: Substantial Revision Required
- **摘要**: We develop a theoretical and computational framework for beam-plasma collective oscillations in intense charged-particle beams at intermediate energies (10-100 MeV). In Part I, we formulate a kinetic field theory governed by the Vlasov-Poisson system, deriving the Lindhard dielectric function and random phase approximation (RPA) polarization tensor for three beam distribution functions. We prove via the dielectric function epsilon(omega,q)=0 the existence of undamped Langmuir wave modes above a critical beam density n_c, obtain explicit beam-plasma dispersion relations, and show that Landau damping vanishes above the particle-hole continuum. The plasma frequency Omega_p^2 = ne^2/(m*epsilon_0) is fixed by the f-sum rule independently of distribution shape; higher dispersion coefficients depend on velocity moments. Space charge effects drive anomalous beam broadening with sqrt(n-n_c) onset and Friedel oscillations at q=2k_F. The beam-plasma transition belongs to the 3D Ising universality class via renormalization group analysis. In Part II, we validate these predictions using Prometheus, a beta-VAE trained on static structure factor data S(q) from particle-in-cell (PIC) beam simulations. Prometheus detects collective plasma oscillation onset in Gaussian and uniform distributions, confirms their absence in the degenerate Fermi gas (n_c -> 0), and resolves the Kohn anomaly at q=2k_F. Dispersion analysis of S(q,omega) from PIC simulations verifies the distribution-independent Omega_p predicted by the f-sum rule. All six validation checks pass. Predicted signatures -- density-tunable plasma resonances at omega_p proportional to sqrt(n), anomalous beam broadening with sqrt(n-n_c) onset, and Friedel oscillations -- are accessible at existing intermediate-energy beam facilities.
- **核心创新**（待 agent 提炼）: 

### 46. Cross-Modal Mapping and Dual-Branch Reconstruction for 2D-3D Multimodal Industrial Anomaly Detection

- **arXiv**: [2603.03939v1](http://arxiv.org/abs/2603.03939v1)
- **提交日期**: 2026-03-04
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Multimodal industrial anomaly detection benefits from integrating RGB appearance with 3D surface geometry, yet existing \emph{unsupervised} approaches commonly rely on memory banks, teacher-student architectures, or fragile fusion schemes, limiting robustness under noisy depth, weak texture, or missing modalities. This paper introduces \textbf{CMDR-IAD}, a lightweight and modality-flexible unsupervised framework for reliable anomaly detection in 2D+3D multimodal as well as single-modality (2D-only or 3D-only) settings. \textbf{CMDR-IAD} combines bidirectional 2D$\leftrightarrow$3D cross-modal mapping to model appearance-geometry consistency with dual-branch reconstruction that independently captures normal texture and geometric structure. A two-part fusion strategy integrates these cues: a reliability-gated mapping anomaly highlights spatially consistent texture-geometry discrepancies, while a confidence-weighted reconstruction anomaly adaptively balances appearance and geometric deviations, yielding stable and precise anomaly localization even in depth-sparse or low-texture regions. On the MVTec 3D-AD benchmark, CMDR-IAD achieves state-of-the-art performance while operating without memory banks, reaching 97.3\% image-level AUROC (I-AUROC), 99.6\% pixel-level AUROC (P-AUROC), and 97.6\% AUPRO. On a real-world polyurethane cutting dataset, the 3D-only variant attains 92.6\% I-AUROC and 92.5\% P-AUROC, demonstrating strong effectiveness under practical industrial conditions. These results highlight the framework's robustness, modality flexibility, and the effectiveness of the proposed fusion strategies for industrial visual inspection. Our source code is available at https://github.com/ECGAI-Research/CMDR-IAD/
- **核心创新**（待 agent 提炼）: 

### 47. Towards an Incremental Unified Multimodal Anomaly Detection: Augmenting Multimodal Denoising From an Information Bottleneck Perspective

- **arXiv**: [2603.02629v1](http://arxiv.org/abs/2603.02629v1)
- **提交日期**: 2026-03-03
- **分类**: cs.CV
- **Comment**: —
- **摘要**: The quest for incremental unified multimodal anomaly detection seeks to empower a single model with the ability to systematically detect anomalies across all categories and support incremental learning to accommodate emerging objects/categories. Central to this pursuit is resolving the catastrophic forgetting dilemma, which involves acquiring new knowledge while preserving prior learned knowledge. Despite some efforts to address this dilemma, a key oversight persists: ignoring the potential impact of spurious and redundant features on catastrophic forgetting. In this paper, we delve into the negative effect of spurious and redundant features on this dilemma in incremental unified frameworks, and reveal that under similar conditions, the multimodal framework developed by naive aggregation of unimodal architectures is more prone to forgetting. To address this issue, we introduce a novel denoising framework called IB-IUMAD, which exploits the complementary benefits of the Mamba decoder and information bottleneck fusion module: the former dedicated to disentangle inter-object feature coupling, preventing spurious feature interference between objects; the latter serves to filter out redundant features from the fused features, thus explicitly preserving discriminative information. A series of theoretical analyses and experiments on MVTec 3D-AD and Eyecandies datasets demonstrates the effectiveness and competitive performance of IB-IUMAD.
- **核心创新**（待 agent 提炼）: 

### 48. Modelling and Simulation of Neuromorphic Datasets for Anomaly Detection in Computer Vision

- **arXiv**: [2602.23514v1](http://arxiv.org/abs/2602.23514v1)
- **提交日期**: 2026-02-26
- **分类**: cs.CV
- **Comment**: draft paper
- **摘要**: Limitations on the availability of Dynamic Vision Sensors (DVS) present a fundamental challenge to researchers of neuromorphic computer vision applications. In response, datasets have been created by the research community, but often contain a limited number of samples or scenarios. To address the lack of a comprehensive simulator of neuromorphic vision datasets, we introduce the Anomalous Neuromorphic Tool for Shapes (ANTShapes), a novel dataset simulation framework. Built in the Unity engine, ANTShapes simulates abstract, configurable 3D scenes populated by objects displaying randomly-generated behaviours describing attributes such as motion and rotation. The sampling of object behaviours, and the labelling of anomalously-acting objects, is a statistical process following central limit theorem principles. Datasets containing an arbitrary number of samples can be created and exported from ANTShapes, along with accompanying label and frame data, through the adjustment of a limited number of parameters within the software. ANTShapes addresses the limitations of data availability to researchers of event-based computer vision by allowing for the simulation of bespoke datasets to suit purposes including object recognition and localisation alongside anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 49. Advancing Industry 4.0: Multimodal Sensor Fusion for AI-Based Fault Detection in 3D Printing

- **arXiv**: [2602.16108v2](http://arxiv.org/abs/2602.16108v2)
- **提交日期**: 2026-02-18
- **分类**: eess.SP
- **Comment**: International Journal of Engineering Research and Innovation | v17, n2, Fall/Winter 2025
- **摘要**: Additive manufacturing, particularly fused deposition modeling, is transforming modern production by enabling rapid prototyping and complex part fabrication. However, its layer-by-layer process remains vulnerable to faults such as nozzle clogging, filament runout, and layer misalignment, which compromise print quality and reliability. Traditional inspection methods are costly, time-intensive, and often limited to post-process analysis, making them unsuitable for real-time intervention. In this current study, the authors developed a novel, low-cost, and portable faultdetection system that leverages multimodal sensor fusion and artificial intelligence for real-time monitoring in FDM-based 3D printing. The system integrates acoustic, vibration, and thermal sensing into a non-intrusive architecture, capturing complementary data streams that reflect both mechanical and process-related anomalies. Acoustic and thermal sensors operate in a fully contactless manner, while the vibration sensor requires minimal attachment such that it will not interfere with printer hardware, thereby preserving portability and ease of deployment. The multimodal signals are processed into spectrograms and time-frequency features, which are classified using convolutional neural networks for intelligent fault detection. The proposed system advances Industry 4.0 objectives by offering an affordable, scalable, and practical monitoring solution that improves faultdetection accuracy, reduces waste, and supports sustainable, adaptive manufacturing.
- **核心创新**（待 agent 提炼）: 

### 50. Generative Latent Representations of 3D Brain MRI for Multi-Task Downstream Analysis in Down Syndrome

- **arXiv**: [2602.13731v1](http://arxiv.org/abs/2602.13731v1)
- **提交日期**: 2026-02-14
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Generative models have emerged as powerful tools in medical imaging, enabling tasks such as segmentation, anomaly detection, and high-quality synthetic data generation. These models typically rely on learning meaningful latent representations, which are particularly valuable given the high-dimensional nature of 3D medical images like brain magnetic resonance imaging (MRI) scans. Despite their potential, latent representations remain underexplored in terms of their structure, information content, and applicability to downstream clinical tasks. Investigating these representations is crucial for advancing the use of generative models in neuroimaging research and clinical decision-making. In this work, we develop multiple variational autoencoders (VAEs) to encode 3D brain MRI scans into compact latent space representations for generative and predictive applications. We systematically evaluate the effectiveness of the learned representations through three key analyses: (i) a quantitative and qualitative assessment of MRI reconstruction quality, (ii) a visualisation of the latent space structure using Principal Component Analysis, and (iii) downstream classification tasks on a proprietary dataset of euploid and Down syndrome individuals brain MRI scans. Our results demonstrate that the VAE successfully captures essential brain features while maintaining high reconstruction fidelity. The latent space exhibits clear clustering patterns, particularly in distinguishing individuals with Down syndrome from euploid controls.
- **核心创新**（待 agent 提炼）: 

### 51. 3DLAND: 3D Lesion Abdominal Anomaly Localization Dataset

- **arXiv**: [2602.12820v1](http://arxiv.org/abs/2602.12820v1)
- **提交日期**: 2026-02-13
- **分类**: eess.IV
- **Comment**: —
- **摘要**: Existing medical imaging datasets for abdominal CT often lack three-dimensional annotations, multi-organ coverage, or precise lesion-to-organ associations, hindering robust representation learning and clinical applications. To address this gap, we introduce 3DLAND, a large-scale benchmark dataset comprising over 6,000 contrast-enhanced CT volumes with over 20,000 high-fidelity 3D lesion annotations linked to seven abdominal organs: liver, kidneys, pancreas, spleen, stomach, and gallbladder. Our streamlined three-phase pipeline integrates automated spatial reasoning, prompt-optimized 2D segmentation, and memory-guided 3D propagation, validated by expert radiologists with surface dice scores exceeding 0.75. By providing diverse lesion types and patient demographics, 3DLAND enables scalable evaluation of anomaly detection, localization, and cross-organ transfer learning for medical AI. Our dataset establishes a new benchmark for evaluating organ-aware 3D segmentation models, paving the way for advancements in healthcare-oriented AI. To facilitate reproducibility and further research, the 3DLAND dataset and implementation code are publicly available at https://mehrn79.github.io/3DLAND.
- **核心创新**（待 agent 提炼）: 

### 52. Proposal for realizing unpaired Weyl points in a three-dimensional periodically driven optical Raman lattice

- **arXiv**: [2602.11935v2](http://arxiv.org/abs/2602.11935v2)
- **提交日期**: 2026-02-12
- **分类**: cond-mat.quant-gas
- **Comment**: 14 pages, 5 figures, to appear in PRA
- **摘要**: In static lattice systems, the Nielsen-Ninomiya theorem enforces the pairing of Weyl points with opposite chiralities, which precludes the chiral magnetic effect (CME) in equilibrium. Periodic driving provides a viable route to circumvent this no-go constraint. Here, we propose a scheme to realize and control unpaired Weyl points using ultracold atoms in a three-dimensional (3D) optical Raman lattice under continuous periodic driving. By engineering distinct relative symmetries between the lattice and multiple Raman potentials, the configuration generates an effective 3D spin-orbit coupling and yields a tunable topological-insulator phase. Through adiabatic periodic modulation of this system, we show that eight Weyl points emerge in the quasienergy spectrum of the low-energy sector, whose net chirality can be precisely tuned. A nonzero total chirality directly corresponds to the formation of unpaired Weyl points. Furthermore, by implementing a synthetic magnetic field via laser-assisted tunneling in this setup, we demonstrate that the chirality imbalance drives a quantized charge current in the weak-field regime, providing a direct signature of the CME. We verify that the adiabatic condition of the driving protocol, as well as the proposed experimental preparation and detection techniques, are within reach of current ultracold-atom experiments. This work establishes a realistic and controllable platform for exploring chiral-anomaly physics and nonequilibrium topological phenomena linked to Weyl fermions.
- **核心创新**（待 agent 提炼）: 

### 53. PRISM: A 3D Probabilistic Neural Representation for Interpretable Shape Modeling

- **arXiv**: [2602.11467v2](http://arxiv.org/abs/2602.11467v2)
- **提交日期**: 2026-02-12
- **分类**: cs.LG
- **Comment**: ICML 2026, camera-ready version, 24 pages
- **摘要**: Understanding how anatomical shapes evolve in response to developmental covariates - and quantifying their spatially varying uncertainties - is critical in healthcare research. Existing approaches typically rely on global time-warping formulations that ignore spatially heterogeneous dynamics. We introduce PRISM, a novel framework that bridges implicit neural representations with uncertainty-aware statistical shape analysis. PRISM models the conditional distribution of shapes given covariates, providing spatially continuous estimates of both the population mean and covariate-dependent uncertainty at arbitrary locations. A key theoretical contribution is a closed-form Fisher Information metric that enables efficient, analytically tractable local temporal uncertainty quantification via automatic differentiation. Experiments on three synthetic datasets and one clinical dataset demonstrate PRISM's strong performance across diverse tasks - from modeling shape evolution to personalized shape prediction and anomaly detection - within a unified framework, while providing interpretable and clinically meaningful uncertainty estimates.
- **核心创新**（待 agent 提炼）: 

### 54. DMP-3DAD: Cross-Category 3D Anomaly Detection via Realistic Depth Map Projection with Few Normal Samples

- **arXiv**: [2602.10806v1](http://arxiv.org/abs/2602.10806v1)
- **提交日期**: 2026-02-11
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Cross-category anomaly detection for 3D point clouds aims to determine whether an unseen object belongs to a target category using only a few normal examples. Most existing methods rely on category-specific training, which limits their flexibility in few-shot scenarios. In this paper, we propose DMP-3DAD, a training-free framework for cross-category 3D anomaly detection based on multi-view realistic depth map projection. Specifically, by converting point clouds into a fixed set of realistic depth images, our method leverages a frozen CLIP visual encoder to extract multi-view representations and performs anomaly detection via weighted feature similarity, which does not require any fine-tuning or category-dependent adaptation. Extensive experiments on the ShapeNetPart dataset demonstrate that DMP-3DAD achieves state-of-the-art performance under few-shot setting. The results show that the proposed approach provides a simple yet effective solution for practical cross-category 3D anomaly detection.
- **核心创新**（待 agent 提炼）: 

### 55. Inlier-Centric Post-Training Quantization for Object Detection Models

- **arXiv**: [2602.03472v1](http://arxiv.org/abs/2602.03472v1)
- **提交日期**: 2026-02-03
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Object detection is pivotal in computer vision, yet its immense computational demands make deployment slow and power-hungry, motivating quantization. However, task-irrelevant morphologies such as background clutter and sensor noise induce redundant activations (or anomalies). These anomalies expand activation ranges and skew activation distributions toward task-irrelevant responses, complicating bit allocation and weakening the preservation of informative features. Without a clear criterion to distinguish anomalies, suppressing them can inadvertently discard useful information. To address this, we present InlierQ, an inlier-centric post-training quantization approach that separates anomalies from informative inliers. InlierQ computes gradient-aware volume saliency scores, classifies each volume as an inlier or anomaly, and fits a posterior distribution over these scores using the Expectation-Maximization (EM) algorithm. This design suppresses anomalies while preserving informative features. InlierQ is label-free, drop-in, and requires only 64 calibration samples. Experiments on the COCO and nuScenes benchmarks show consistent reductions in quantization error for camera-based (2D and 3D) and LiDAR-based (3D) object detection.
- **核心创新**（待 agent 提炼）: 

### 56. Is Task-Specific Training Necessary for Anomaly Detection?

- **arXiv**: [2601.22763v3](http://arxiv.org/abs/2601.22763v3)
- **提交日期**: 2026-01-30
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Current state-of-the-art multi-class unsupervised anomaly detection (MUAD) methods rely on training encoder--decoder models to reconstruct anomaly-free features. However, we argue that such task-specific training is costly under distribution shifts, and that reconstruction-based residual scoring further faces a fidelity--stability dilemma. Existing training-free alternatives, in turn, remain prone to cross-category and cross-region mismatches in MUAD. Motivated by these limitations, we propose Retrieval-based Anomaly Detection (RAD), a task-specific training-free framework that stores anomaly-free features in a memory and detects anomalies through multi-level retrieval, matching test patches against the memory. Experiments demonstrate that RAD achieves state-of-the-art performance across four established benchmarks (MVTec-AD, VisA, Real-IAD, 3D-ADAM) under both standard and few-shot settings. On MVTec-AD, RAD reaches 96.7% Pixel AUROC with just a single anomaly-free image compared to 98.5% of RAD's full-data performance. Collectively, these findings overturn the assumption that MUAD requires task-specific training, showing that state-of-the-art anomaly detection is feasible with training-free memory-based retrieval. Our code is available at https://github.com/longkukuhi/RAD.
- **核心创新**（待 agent 提炼）: 

### 57. Detection of Gravitational Anomaly at Low Acceleration from a Highest-quality Sample of 36 Wide Binaries with Accurate 3D Velocities

- **arXiv**: [2601.21728v3](http://arxiv.org/abs/2601.21728v3)
- **提交日期**: 2026-01-29
- **分类**: astro-ph.GA
- **Comment**: 41 pages (main part) + 39 pages (appendix), revised version for the AAS journals
- **摘要**: We set out to accurately measure gravity in the low-acceleration range $(10^{-11},10^{-9})\,{\rm m}\,{\rm s}^{-2}$ from 3D motions of isolated wide binary stars. Gaia DR3 provides precise measurements of the four sky-plane components of the 3D relative displacement and velocity ($\mathbf{r}, \mathbf{v}$) for a wide binary, but not comparably precise line-of-sight (radial) separation and relative velocity $v_{r}$. Based on our new observations and the public databases/publications, we assemble a sample of 36 nearby (distance $<150$pc) wide binaries in the low-acceleration regime with accurate values of $v_{r}$ (measurement uncertainty $< 100$ m\,s$^{-1}$). Kinematic contaminants such as undetected stellar companions are well under control using various observational diagnostics such as Gaia's {\tt ruwe} parameter, the color-magnitude diagram, multi-epoch observations of radial velocities, Speckle interferometric follow-up observations, and requiring Hipparcos-Gaia proper motion consistency. For the parameter $Γ\equiv \log_{10}\sqrtγ$ with $γ\equiv G/G_{\rm N}$ (where $G$ is a parameter generalizing Newton's constant $G_{\rm N}$ in elliptical orbits), we find $Γ=0.102_{-0.021}^{+0.028}$ for $<10^{-9.1}\,{\rm m}\,{\rm s}^{-2}$ ($0.132_{-0.027}^{+0.035}$ for $<10^{-9.5}\,{\rm m}\,{\rm s}^{-2}$) giving a gravity boost factor of $γ=1.60_{-0.14}^{+0.24}$, which rules out Newton and is higher than relevant MOND predictions. This strong anomaly is dominated by two systems (the pairs of HD 189739, HD 189760, and TYC 259-236-1, TYC 259-906-1) that have 3D relative velocities exceeding their estimated Newtonian escape velocities but are unlikely to be chance associations or contaminated systems. (abridged)
- **核心创新**（待 agent 提炼）: 

### 58. Test-Time Adaptation for Anomaly Segmentation via Topology-Aware Optimal Transport Chaining

- **arXiv**: [2601.20333v1](http://arxiv.org/abs/2601.20333v1)
- **提交日期**: 2026-01-28
- **分类**: cs.CV
- **Comment**: —
- **摘要**: Deep topological data analysis (TDA) offers a principled framework for capturing structural invariants such as connectivity and cycles that persist across scales, making it a natural fit for anomaly segmentation (AS). Unlike thresholdbased binarisation, which produces brittle masks under distribution shift, TDA allows anomalies to be characterised as disruptions to global structure rather than local fluctuations. We introduce TopoOT, a topology-aware optimal transport (OT) framework that integrates multi-filtration persistence diagrams (PDs) with test-time adaptation (TTA). Our key innovation is Optimal Transport Chaining, which sequentially aligns PDs across thresholds and filtrations, yielding geodesic stability scores that identify features consistently preserved across scales. These stabilityaware pseudo-labels supervise a lightweight head trained online with OT-consistency and contrastive objectives, ensuring robust adaptation under domain shift. Across standard 2D and 3D anomaly detection benchmarks, TopoOT achieves state-of-the-art performance, outperforming the most competitive methods by up to +24.1% mean F1 on 2D datasets and +10.2% on 3D AS benchmarks.
- **核心创新**（待 agent 提炼）: 

### 59. 3D-SONAR: Self-Organizing Network for 3D Anomaly Ranking

- **arXiv**: [2601.09294v1](http://arxiv.org/abs/2601.09294v1)
- **提交日期**: 2026-01-14
- **分类**: stat.AP
- **Comment**: 28 pages, 12 figures
- **摘要**: Surface anomaly detection using 3D point cloud data has gained increasing attention in industrial inspection. However, most existing methods rely on deep learning techniques that are highly dependent on large-scale datasets for training, which are difficult and expensive to acquire in real-world applications. To address this challenge, we propose a novel method based on self-organizing network for 3D anomaly ranking, also named 3D-SONAR. The core idea is to model the 3D point cloud as a dynamic system, where the points are represented as an undirected graph and interact via attractive and repulsive forces. The energy distribution induced by these forces can reveal surface anomalies. Experimental results show that our method achieves superior anomaly detection performance in both open surface and closed surface without training. This work provides a new perspective on unsupervised inspection and highlights the potential of physics-inspired models in industrial anomaly detection tasks with limited data.
- **核心创新**（待 agent 提炼）: 

### 60. TRACE: Reconstruction-Based Anomaly Detection in Ensemble and Time-Dependent Simulations

- **arXiv**: [2601.08659v1](http://arxiv.org/abs/2601.08659v1)
- **提交日期**: 2026-01-13
- **分类**: cs.LG
- **Comment**: —
- **摘要**: Detecting anomalies in high-dimensional, time-dependent simulation data is challenging due to complex spatial and temporal dynamics. We study reconstruction-based anomaly detection for ensemble data from parameterized Kármán vortex street simulations using convolutional autoencoders. We compare a 2D autoencoder operating on individual frames with a 3D autoencoder that processes short temporal stacks. The 2D model identifies localized spatial irregularities in single time steps, while the 3D model exploits spatio-temporal context to detect anomalous motion patterns and reduces redundant detections across time. We further evaluate volumetric time-dependent data and find that reconstruction errors are strongly influenced by the spatial distribution of mass, with highly concentrated regions yielding larger errors than dispersed configurations. Our results highlight the importance of temporal context for robust anomaly detection in dynamic simulations.
- **核心创新**（待 agent 提炼）: 
