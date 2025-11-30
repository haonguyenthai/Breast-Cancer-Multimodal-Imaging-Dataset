Nice, repo nhìn xịn rồi đó 😎
Tớ viết lại README.md cho khớp với datasets_master.csv + các hình mà m đã generate (histogram, pie, subjects bar, datatype bar/pie, multimodal heatmap). M chỉ cần copy–paste đè file README hiện tại.

⸻


# Breast-Cancer-Multimodal-Imaging-Datasets

Credit: This repo inherits and extends some of the summaries from  
https://github.com/hugofigueiras/Breast-Cancer-Imaging-Datasets

This repository serves as a centralized resource listing **breast imaging and pathology datasets** commonly used in academic research, clinical training, and machine-learning applications. The goal is to provide in one place:

- A curated list of datasets across **radiology (MRI, MG/DBT, US, CT, PET)**,  
  **histopathology / whole-slide images**, and **multimodal** resources.
- High-level metadata (number of subjects, data types, supporting clinical / omics data).
- Pointers on _how to obtain_ each dataset.

If you know more datasets and want to contribute, please submit a pull request – contributions are very welcome 😊

All datasets are catalogued in:

```text
data/datasets_master.csv

Currently the CSV contains 65+ datasets spanning radiology, histopathology and multimodal (imaging + clinical / omics) resources.

⸻

Overview

The figures below summarize the contents of datasets_master.csv.

Number of datasets per modality group:

Pie chart – distribution of datasets by modality group:

Here, ModalityGroup is a coarse grouping:
	•	MRI, Mammography, Ultrasound, DBT – radiology modalities
	•	Histopathology – histology / WSI / patch-level pathology datasets
	•	Multimodal – datasets that combine ≥2 imaging modalities and/or imaging with omics/clinical data

Total number of subjects per modality group:

For histopathology datasets where only the number of slides is reported, slides are treated as a proxy for subjects.

Datasets by data type (radiology, WSI, omics, clinical/report):

This bar plot counts, for each dataset, whether it contains:
	•	MRI
	•	Mammography / DBT
	•	Ultrasound
	•	CT
	•	PET
	•	Histopathology / WSI
	•	Omics (genomics, proteomics, molecular tests)
	•	Clinical / Report (demographics, diagnosis, follow-up, treatment, pathology report, etc.)

A single dataset can contribute to multiple categories (e.g. MRI + WSI + omics).

If you generated the additional pie chart for data types:


⸻

Table of Contents
	•	Datasets
	•	Ultrasound
	•	Digital Breast Tomosynthesis (DBT)
	•	Mammography
	•	MRI
	•	Histopathology
	•	Repository structure
	•	Contributing & Contact

⸻

Datasets

🔎 Full list: for the most up-to-date and complete metadata (including multimodal and histopathology / WSI datasets), please refer to
data/datasets_master.csv.
The tables below highlight the main public radiology datasets.

Ultrasound

Dataset	Subjects	Nº Samples	Format	Size	Year	Cite	Access data	Paired	Note
Breast Ultrasound Images (BUSI)	600	780	PNG	204MB	2020	Dataset of breast ultrasound images	Download here	No	Has ground-truth masks; labels: benign, malignant, normal
Breast Lesions USG	256	522	PNG	66.67MB	2024	Curated benchmark dataset for ultrasound based breast lesion analysis	Download here	Clinical	Patient-level labels, image-level annotations, and tumour-level labels with all cases confirmed by follow-up or core-needle biopsy
UDIAT Breast Ultrasound Dataset B	163	163	N/A	N/A	2017	Automated Breast Ultrasound Lesions Detection Using Convolutional Neural Networks	Request permission	No	–
OASBUD	78	200	Matlab	296.8MB	2017	Open access database of raw ultrasonic signals acquired from malignant and benign breast lesions	Download here	No	Raw RF signals for advanced ultrasound processing
BUS Synthetic Dataset	0	500	PNG	9.7MB	2023	PDF-UNet: A semi-supervised method for segmentation of breast tumor images using a U-shaped pyramid-dilated network	Download here	No	Synthetic BUS images for segmentation / augmentation

Summaries
	•	BUSI: Small (~500×500) ultrasound images for benign vs malignant classification and segmentation.
	•	Breast Lesions USG: Curated benchmark with detailed lesion-level annotations.
	•	UDIAT Dataset B: Classical dataset for ultrasound lesion detection / classification.
	•	OASBUD: Raw RF signals enabling signal-processing-oriented work.
	•	BUS Synthetic Dataset: Synthetic images for semi-supervised segmentation and data augmentation.

⸻

Digital Breast Tomosynthesis (DBT)

Dataset	Subjects	Nº Samples	Format	Size	Year	Cite	Download
Breast Cancer Screening DBT	5,060	22,032	DICOM	1.63TB	2024	A Data Set and Deep Learning Algorithm for the Detection of Masses and Architectural Distortions in Digital Breast Tomosynthesis Images	Download here
EA1141	1,444	500	DICOM	2.82TB	2023	Abbreviated Breast MRI and Digital Tomosynthesis Mammography in Screening Women With Dense Breasts (EA1141) (dataset)	Download here
VICTRE	2,994	2,994	DICOM	1.03TB	2019	The VICTRE Trial: Open-Source, In-Silico Clinical Trial for Evaluating Digital Breast Tomosynthesis	Download here

Summaries
	•	Breast Cancer Screening DBT: High-resolution DBT volumes for mass / architectural distortion detection.
	•	EA1141: DBT paired with abbreviated MRI in dense-breast screening.
	•	VICTRE: Fully simulated DBT for in-silico trials and CAD evaluation.

⸻

Mammography

Dataset	Subjects	Nº Samples	Format	Size	Year	Cite	Download
CBIS-DDSM	1,566	6,671	DICOM	161.51GB	2017	A curated mammography data set for use in computer-aided detection and diagnosis research	Download here
CMMD	1,775	3,728	DICOM	22.86GB	2021	The Chinese Mammography Database (CMMD)	Download here
CDD-CESM	326	2,006	JPEG	1.5GB	2021	Categorized Contrast Enhanced Mammography dataset and related papers	Download here
VinDr-Mammo	5,000	20,000	DICOM	N/A	2022	A large-scale benchmark dataset for CAD in full-field digital mammography	Download here
INBreast	115	410	N/A	N/A	2012	INbreast: toward a full-field digital mammographic database	Contact the authors
MIAS	N/A	322	PGM	1.5GB	2015	MIAS database v1.21	Download here
Breast Tumor Mammography Dataset for Computer Vision	N/A	3,383	JPG	103.49MB	2024	N/A	Download here

Summaries
	•	CBIS-DDSM: Annotated mammograms for classification, calcification detection, and mass segmentation.
	•	CMMD: Chinese cohort with biopsy-confirmed labels for cross-population studies.
	•	CDD-CESM: Low-energy and subtracted CESM images for contrast-enhanced analysis.
	•	VinDr-Mammo: Large-scale mammography benchmark with rich labels.
	•	INBreast: High-quality FFDM dataset often used for benchmarking.
	•	MIAS: Classic low-resolution dataset, good for didactic examples.
	•	Breast Tumor Mammography Dataset: Smaller Kaggle dataset for quick experiments.

⸻

MRI

Dataset	Subjects	Nº Samples	Format	Size	Year	Cite	Download
ACRIN-6667	984	984	DICOM	199.59GB	2021	ACRIN-Contralateral-Breast-MR (ACRIN 6667)	Download here
ACRIN-6698	385	385	DICOM	1.94TB	2021	ACRIN 6698/I-SPY2 Breast DWI	Download here
ISPY1	222	222	DICOM	78.36GB	2016	I-SPY1 / ACRIN 6657 DCE-MRI	Download here
ISPY2	719	719	DICOM	4.16TB	2022	I-SPY2 Breast DCE-MRI trial	Download here
Duke Breast Cancer MRI	922	922	DICOM	368.89GB	2022	Radiogenomics of breast cancer with 922 subjects	Download here
Breast Cancer Patients MRI’s	700	700	JPG	201.4MB	2021	N/A	Download here
Breast MRI NACT Pilot	64	64	DICOM	19.51GB	2023	Single site breast DCE-MRI NACT data	Download here
QIN Breast DCE-MRI	10	10	DICOM	15.9GB	2019	QIN Breast DCE-MRI challenge	Download here
QIN-BREAST	67	67	DICOM	11.41GB	2020	Data From QIN-BREAST (Version 2)	Download here
QIN-BREAST-02	13	13	DICOM	4.19GB	2019	Data from QIN-BREAST-02	Download here
Advanced MRI Breast Lesions	632	632	DICOM	646GB	2024	Advanced-MRI-Breast-Lesions	Download here
BREAST DIAGNOSIS	88	88	DICOM	60.87GB	2011	BREAST-DIAGNOSIS dataset	Download here

Summaries
	•	ACRIN-6667 / 6698 & ISPY1 / ISPY2: Multi-centre trials for neoadjuvant chemotherapy response; ideal for longitudinal / predictive modelling.
	•	Duke Breast Cancer MRI: Radiogenomics-oriented dataset with rich imaging features.
	•	QIN- datasets:* Smaller but high-quality cohorts for biomarker evaluation and treatment-response modelling.
	•	Advanced MRI Breast Lesions & BREAST-DIAGNOSIS: Rich clinical and imaging metadata for lesion characterisation and classification.

⸻

Histopathology

Histopathology / WSI datasets (e.g. TCGA-BRCA, CPTAC-BRCA, CAMELYON, BRACS, TUPAC16, NuCLS, BCSS, DROID-Breast, ACROBAT, GTEx, Prov-Path, etc.) are all integrated into:

data/datasets_master.csv

For more detailed notes, including pretraining / benchmarking usage within my projects, see also:
https://github.com/haonguyenthai/Breast-Cancer-Pathology-Dataset

⸻

Repository structure
	•	data/datasets_master.csv – master table with all datasets and metadata.
	•	scripts/generate_figures.py – generates summary figures (modality histogram, pie charts, subject distribution, data-type bar/pie).
	•	images/ – rendered figures used in this README.
	•	Additional scripts (e.g. plot_multimodal_matrix.py, plot_multimodal_cohort_counts.py) – visualize intersections between imaging, histopathology, omics and clinical data across cohorts.

⸻

Contributing & Contact
	•	Contributions
Suggestions for new datasets, corrections, or improvements to the metadata / scripts are welcome. Please open an issue or submit a pull request.
	•	Contact
For dataset access, follow the official links provided in the tables and CSV, or contact dataset maintainers directly.
For questions about this repository, feel free to email me at
hao.nguyen@uq.edu.au.

Nếu m có thêm hình khác (VD: multimodal heatmap `multimodal_matrix.png`, `multimodal_cohort_counts.png`), gửi tên file cho t, t nhét thêm 1 section “Multimodal intersections” với caption đẹp cho m luôn.
