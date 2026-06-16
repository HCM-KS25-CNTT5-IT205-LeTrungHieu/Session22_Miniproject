import logging

# 3.2. Quản lý hệ thống bằng Module Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- CÁC HÀM XỬ LÝ NGHIỆP VỤ ---


def show_devices(devices_list):
    """2.1. Chức năng 1: Xem danh sách thiết bị giám sát"""
    logger.debug(f"Đang truy vấn hiển thị cho {len(devices_list)} thiết bị")
    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    # Căn lề dữ liệu bằng f-string (căn trái chữ, căn phải số)
    print(f"\n{'-'*95}")
    print(
        f"{'MÃ THIẾT BỊ':<12} | {'VỊ TRÍ PHÂN XƯỞNG':<25} | {'CHỈ SỐ CŨ':>12} | {'CHỈ SỐ MỚI':>12} | {'TRẠNG THÁI':<12}"
    )
    print(f"{'-'*95}")
    for d in devices_list:
        print(
            f"{d['id']:<12} | {d['location']:<25} | {d['old_index']:>12.2f} | {d['new_index']:>12.2f} | {d['status']:<12}"
        )
    print(f"{'-'*95}\n")


def update_indices(devices_list):
    """2.2. Chức năng 2: Cập nhật chỉ số điện tiêu thụ (Check-in số liệu)"""
    device_id = input("Nhập mã thiết bị cần cập nhật chỉ số: ")

    # Tìm kiếm thiết bị
    device = None
    for d in devices_list:
        if d["id"] == device_id:
            device = d
            break

    if not device:
        print(
            "[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!"
        )
        return

    # Nhập và xác thực chỉ số cũ
    while True:
        try:
            old_idx = float(input("Nhập chỉ số cũ: "))
            if old_idx < 0:
                print(
                    "[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!"
                )
                continue
            break
        except ValueError:
            logger.error("[Lỗi]: Kỹ thuật viên nhập sai định dạng số tại ô chỉ số điện")
            print(
                "[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!"
            )

    # Nhập và xác thực chỉ số mới
    while True:
        try:
            new_idx = float(input("Nhập chỉ số mới: "))
            if new_idx < 0:
                print(
                    "[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!"
                )
                continue
            if new_idx < old_idx:
                print(
                    "[Lỗi] (ERR-E02): Số liệu lỗi! Chỉ số mới không được nhỏ hơn chỉ số cũ!"
                )
                continue
            break
        except ValueError:
            logger.error("[Lỗi]: Kỹ thuật viên nhập sai định dạng số tại ô chỉ số điện")
            print(
                "[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!"
            )

    # Cập nhật vào danh sách
    device["old_index"] = old_idx
    device["new_index"] = new_idx
    logger.info(f"[Thành công]: Đã check-in số liệu cho thiết bị {device_id}")
    print(f"[Thành công]: Đã cập nhật thành công chỉ số cho {device_id}.")


def trigger_overload_alert(devices_list):
    """2.3. Chức năng 3: Kích hoạt trạng thái cảnh báo quá tải"""
    device_id = input("Nhập mã thiết bị cần cảnh báo: ")

    device = None
    for d in devices_list:
        if d["id"] == device_id:
            device = d
            break

    if not device:
        print(
            "[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!"
        )
        return

    consumption = device["new_index"] - device["old_index"]

    if consumption > 5000:
        if device["status"] == "Normal":
            device["status"] = "Overload"
            logger.warning(
                f"[Cảnh báo]: Thiết bị {device_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!"
            )
            print(
                f"[Thành công]: Thiết bị {device_id} đã được chuyển sang trạng thái OVERLOAD"
            )
        elif device["status"] == "Overload":
            print(
                "[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!"
            )
    else:
        print(
            f"Thiết bị {device_id} có mức tiêu thụ ({consumption} kWh) nằm trong mức an toàn."
        )


def calculate_energy_financials(devices_list):
    """
    2.4. Chức năng 4: Tính tổng lượng điện & Chi phí năng lượng
    Tuyệt đối không in (print) kết quả trực tiếp trong hàm này.
    Chỉ trả về Tuple: (tong_kwh_tieu_thu, phan_tram_chiet_khau, tong_tien_sau_chiet_khau)
    """
    logger.debug(f"Đang tính toán chi phí năng lượng cho {len(devices_list)} thiết bị")

    if not devices_list:
        return (0.0, 0.0, 0.0)

    total_kwh = sum((d["new_index"] - d["old_index"]) for d in devices_list)

    base_price = 3000
    discount_percent = 0.0

    if total_kwh >= 50000:
        discount_percent = 0.03  # Chiết khấu 3%

    total_cost = total_kwh * base_price * (1 - discount_percent)

    return (float(total_kwh), float(discount_percent), float(total_cost))


# --- HÀM ĐIỀU PHỐI CHÍNH ---


def main():
    # 4. Đặc tả dữ liệu: Biến kiểu List chứa tập hợp các Dictionary thiết bị
    devices_list = [
        {
            "id": "M01",
            "location": "Xưởng Cơ Khí A",
            "old_index": 1200.0,
            "new_index": 1200.0,
            "status": "Normal",
        },
        {
            "id": "M02",
            "location": "Xưởng Luyện Kim",
            "old_index": 500.0,
            "new_index": 500.0,
            "status": "Normal",
        },
    ]

    while True:
        print("\n" + "=" * 50)
        print("  SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN  ")
        print("=" * 50)
        print("1. Xem danh sách thiết bị giám sát")
        print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
        print("3. Kích hoạt trạng thái cảnh báo quá tải")
        print("4. Tính tổng lượng điện & Chi phí năng lượng")
        print("5. Thoát chương trình")
        print("=" * 50)

        try:
            choice = int(input("Mời chọn chức năng (1-5): "))
        except ValueError:
            print(
                "[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!"
            )
            continue

        if choice == 1:
            show_devices(devices_list)
        elif choice == 2:
            update_indices(devices_list)
        elif choice == 3:
            trigger_overload_alert(devices_list)
        elif choice == 4:
            # Nhận tuple từ hàm tính toán và in tại hàm main
            total_kwh, discount, total_cost = calculate_energy_financials(devices_list)
            print("\n--- BÁO CÁO CHI PHÍ NĂNG LƯỢNG ---")
            print(f"Tổng lượng điện tiêu thụ : {total_kwh:,.2f} kWh")
            print(f"Mức chiết khấu áp dụng    : {discount * 100:.0f}%")
            print(f"Tổng chi phí thanh toán  : {total_cost:,.2f} VND")
            print("----------------------------------")
        elif choice == 5:
            print("Đã thoát chương trình. Chào tạm biệt!")
            break
        else:
            print(
                "[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!"
            )


if __name__ == "__main__":
    main()
