import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd # Thư viện này để làm cái bảng cho đẹp

# 1. Kết nối (Giữ nguyên như cũ)
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://web-ca-nhan-640c4-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# 2. Thiết lập giao diện Sidebar (Cột bên trái)
st.sidebar.title("Menu Quản Lý")
choice = st.sidebar.radio("Chọn chức năng:", ["Nhập khách hàng", "Xem danh sách"])

if choice == "Nhập khách hàng":
    st.title("➕ Thêm Khách Hàng Mới")
    with st.form("input_form"):
        name = st.text_input("Tên:")
        phone = st.text_input("SĐT:")
        submit = st.form_submit_button("Lưu lên Cloud")
        if submit and name and phone:
            db.reference('khach_hang').push({'ten': name, 'sdt': phone})
            st.success("Đã lưu!")

elif choice == "Xem danh sách":
    st.title("📋 Danh Sách Khách Hàng")
    
    # Lấy dữ liệu từ Firebase về
    data = db.reference('khach_hang').get()
    
    if data:
        # Biến dữ liệu JSON thành bảng (DataFrame) để hiển thị
        items = list(data.values())
        df = pd.DataFrame(items)
        
        # Đổi tên cột cho đẹp
        df.columns = ['Số Điện Thoại', 'Họ Tên']
        
        # Hiện cái bảng ra màn hình
        st.table(df)
    else:
        st.info("Chưa có ai trong danh sách hết mày ơi!")