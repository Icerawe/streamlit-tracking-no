import pandas as pd
import random
from faker import Faker

fake = Faker('th_TH')  # ภาษาไทย

# จำนวนข้อมูลที่ต้องการสร้าง
num_students = 100

data = []

for i in range(1, num_students + 1):
    student_id = f"67{str(i).zfill(6)}"
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.street_address()
    district = fake.tambon()
    amphoe = fake.amphoe()
    province = fake.province()
    zip_code = fake.postcode()
    phone = fake.phone_number()
    set_1 = random.choice([0, 1])
    set_2 = random.choice([0, 1]) if not set_1 else 0  # ไม่ให้มีทั้ง set_1 และ set_2 เป็น 1 พร้อมกัน
    status = random.choice(["จัดส่งสำเร็จแล้ว", "อยู่ระหว่างการผลิต", "ยกเลิก"])
    tracking = fake.bothify(text="TH#########")
    faculty = random.choice(["วิศวกรรมศาสตร์", "วิทยาศาสตร์"])
    department = random.choice(["วิศวกรรมซอฟต์แวร์", "วิทยาศาสตร์ข้อมูล"]) if faculty == "วิศวกรรมศาสตร์" else "วิทยาศาสตร์ข้อมูล"

    data.append({
        "รหัสนักศึกษา": student_id,
        "ชื่อ": first_name,
        "นามสกุล": last_name,
        "คณะ": faculty,
        "สาขาวิชา": department,
        "ที่อยู่จัดส่ง": address,
        "ตำบล": district,
        "อำเภอ": amphoe,
        "จังหวัด": province,
        "รหัสไปรษณีย์": zip_code,
        "เบอร์โทรศัพท์": phone,
        "set_1": set_1,
        "set_2": set_2,
        "สถานะ": status,
        "หมายเลขพัสดุ": tracking
    })

# สร้าง DataFrame
df = pd.DataFrame(data)

# แสดงตัวอย่างข้อมูล
print(df.head())

# บันทึกเป็น CSV (ถ้าต้องการ)
df.to_csv("mock_student_data.csv", index=False, encoding='utf-8-sig')