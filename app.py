import streamlit as st
import requests
import pandas as pd

API_KEY = st.secrets['google']["API_KEY"]  # Replace with your API key
SPREADSHEET_ID = st.secrets['google']["SPREADSHEET_ID"]  # Replace with your spreadsheet ID

def determine_concluded(row):
    return ", ".join(
        f"เซตที่ {i}" for i in range(1, 21) if row.get(f"set_{i}") == 1
    )

# --- Load Data from Google Sheets ---
@st.cache_data(ttl=600)
def load_data():
    sheet_name = "template"
    """Fetch data from a specific sheet."""
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{sheet_name}"
        f"?key={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")

    data = response.json().get("values", [])
    if not data:
        return pd.DataFrame()  # Return empty DataFrame if no data

    # Normalize data to match the header length
    max_cols = len(data[0])
    normalized_data = [row + [''] * (max_cols - len(row)) for row in data]
    return pd.DataFrame(normalized_data[1:], columns=normalized_data[0])

# df = load_data()
df = pd.read_csv("mock_student_data.csv")
df["เซต"] = df.apply(determine_concluded, axis=1)

# --- Page Config ---
st.set_page_config(page_title="สุเทพสตูดิโอ เชียงใหม่", layout="centered")

# --- Cover Image ---
st.image("cover.jpg", use_container_width=True)

# --- Titles ---
st.title("สุเทพสตูดิโอ เชียงใหม่")
st.subheader("ตรวจสอบสถานะการจัดส่งรูป บัณฑิตมหาวิทยาลัยแม่โจ้")

# --- Session State Setup ---
if "student_input" not in st.session_state:
    st.session_state.student_input = ""
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

def do_search():
    st.session_state.search_clicked = True

# --- Input Area ---
st.text_input(
    "กรุณาใส่รหัสนักศึกษา",
    key="student_input",
    placeholder="เช่น 67000001, 67000002 หรือ 67000001, 67000002",
    # height=100,
)

# --- Search Button ---
st.button("ค้นหา", on_click=do_search)

# --- Search Logic ---
if st.session_state.search_clicked:
    user_input = st.session_state.student_input.strip()
    if user_input:
        ids = [x.strip() for x in user_input.replace(",", " ").split()]
        filtered = df[df["รหัสนักศึกษา"].astype(str).isin(ids)].copy()

        # เติมหมายเลขพัสดุ
        def get_tracking(row):
            if row["สถานะ"] == "จัดส่งสำเร็จแล้ว":
                return row["หมายเลขพัสดุ"]
            elif row["สถานะ"] == "อยู่ระหว่างการผลิต":
                return "-"
            return ""

        filtered["หมายเลขพัสดุ"] = filtered.apply(get_tracking, axis=1)

        if filtered.empty:
            st.info("ไม่พบข้อมูลรหัสนักศึกษาที่กรอกมา")
        else:
            missing = set(ids) - set(filtered["รหัสนักศึกษา"].astype(str))
            if missing:
                st.warning(f"ไม่พบรหัสนักศึกษาดังต่อไปนี้: {', '.join(missing)}")

            def highlight_status(row):
                if row["สถานะ"] == "จัดส่งสำเร็จแล้ว":
                    return ["background-color: #d4edda"] * len(row)  # Green
                elif row["สถานะ"] == "อยู่ระหว่างการผลิต":
                    return ["background-color: #fff3cd"] * len(row)  # Yellow
                return [""] * len(row)

            st.subheader("ผลการตรวจสอบ")
            styled_df = (
                filtered[
                    [
                        "รหัสนักศึกษา",
                        "สถานะ",
                        "หมายเลขพัสดุ",
                        "ชื่อ",
                        "นามสกุล",
                        "คณะ",
                        "สาขาวิชา",
                        "เซต",
                        "ที่อยู่จัดส่ง",
                        "ตำบล",
                        "อำเภอ",
                        "จังหวัด",
                        "รหัสไปรษณีย์",
                        "เบอร์โทรศัพท์"
                    ]
                ]
                .style
                .apply(highlight_status, axis=1)
                .hide(axis="index")
            )
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("กรุณากรอกรหัสนักศึกษา ก่อนกดค้นหา")