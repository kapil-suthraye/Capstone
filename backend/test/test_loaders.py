from backend.config import (
    MEDICAL_RECORDS_FOLDER,
    GUIDELINES_FOLDER,
    GROUND_TRUTH_FOLDER
)

from backend.loaders.medical_loader import (
    MedicalRecordLoader
)

from backend.loaders.guideline_loader import (
    GuidelineLoader
)

from backend.loaders.groundtruth_loader import (
    GroundTruthLoader
)

print("="*60)
print("Medical Loader")
print("="*60)

medical = MedicalRecordLoader(
    MEDICAL_RECORDS_FOLDER
)

records = medical.get_all_records()

for pdf in records:

    print(pdf.name)

print()

print("="*60)
print("Guideline Loader")
print("="*60)

guidelines = GuidelineLoader(
    GUIDELINES_FOLDER
)

df = guidelines.load()

print(df.head())

print()

print("="*60)
print("Ground Truth")
print("="*60)

gt = GroundTruthLoader(
    GROUND_TRUTH_FOLDER
)

gt_df = gt.load()

print(gt_df.head())