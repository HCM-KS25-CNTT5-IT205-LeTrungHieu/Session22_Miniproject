# Giả sử hàm calculate_energy_financials được import từ file main.py
from main import calculate_energy_financials


def test_empty_devices_list():
    """Test 1: Test danh sách rỗng (test_empty_devices_list)"""
    devices_list = []
    result = calculate_energy_financials(devices_list)
    assert result == (0.0, 0.0, 0.0), "Lỗi: Danh sách rỗng phải trả về (0.0, 0.0, 0.0)"


def test_financials_with_discount():
    """Test 2: Test mốc đạt chiết khấu (test_financials_with_discount) >= 50,000 kWh"""
    devices_list = [
        {
            "id": "M01",
            "location": "Xưởng A",
            "old_index": 1000,
            "new_index": 30000,
            "status": "Normal",
        },  # Tiêu thụ 29,000
        {
            "id": "M02",
            "location": "Xưởng B",
            "old_index": 2000,
            "new_index": 23000,
            "status": "Normal",
        },  # Tiêu thụ 21,000
    ]
    # Tổng tiêu thụ: 50,000 kWh (Đạt mốc >= 50,000)
    # Kỳ vọng: 3% discount -> tiền = 50,000 * 3000 * 0.97 = 145,500,000
    total_kwh, discount, total_cost = calculate_energy_financials(devices_list)

    assert total_kwh == 50000.0
    assert discount == 0.03
    assert total_cost == 145500000.0


def test_financials_no_discount():
    """Test 3: Test mốc không đạt chiết khấu (test_financials_no_discount) < 50,000 kWh"""
    devices_list = [
        {
            "id": "M01",
            "location": "Xưởng A",
            "old_index": 0,
            "new_index": 49999,
            "status": "Normal",
        }  # Tiêu thụ 49,999
    ]
    # Tổng tiêu thụ: 49,999 kWh (Không đạt mốc)
    # Kỳ vọng: 0% discount -> tiền = 49,999 * 3000 = 149,997,000
    total_kwh, discount, total_cost = calculate_energy_financials(devices_list)

    assert total_kwh == 49999.0
    assert discount == 0.0
    assert total_cost == 149997000.0
