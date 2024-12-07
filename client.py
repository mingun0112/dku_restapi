import requests
import os

BASE_URL = "http://127.0.0.1:8000/api/bookings"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_booking():
    clear_screen()
    print("=== 예약 생성 ===")
    patient_name = input("환자 이름: ")
    patient_phone = input("환자 전화번호: ")
    while True:
        try:
            doctor_id = int(input("의사 ID: "))
            break
        except ValueError:
            print("잘못된 입력입니다. 의사 ID는 숫자로 입력하세요.")
    date = input("예약 날짜 (YYYY-MM-DD): ")
    time = input("예약 시간 (HH:MM): ")
    
    payload = {
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "doctor_id": doctor_id,
        "date": date,
        "time": time,
    }
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print("\n[성공] 예약이 성공적으로 생성되었습니다.")
        print(response.json())
    else:
        print("\n[실패] 예약 생성에 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def get_bookings():
    clear_screen()
    print("=== 예약 목록 조회 ===")
    doctor_id = input("의사 ID (선택사항, 엔터로 넘기기): ")
    date = input("예약 날짜 (선택사항, 엔터로 넘기기): ")

    params = {}
    if doctor_id:
        try:
            params["doctor_id"] = int(doctor_id)
        except ValueError:
            print("잘못된 입력입니다. 의사 ID는 숫자로 입력하세요.")
            return
    if date:
        params["date"] = date

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        print("\n[성공] 예약 목록:")
        for booking in response.json():
            print(f"ID: {booking['id']}, 환자: {booking['patient_name']}, 날짜: {booking['date']}, 상태: {booking['status']}")
    else:
        print("\n[실패] 예약 목록 조회에 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def get_booking():
    clear_screen()
    print("=== 예약 상세 조회 ===")
    while True:
        try:
            booking_id = int(input("조회할 예약 ID: "))
            break
        except ValueError:
            print("잘못된 입력입니다. 예약 ID는 숫자로 입력하세요.")
    url = f"{BASE_URL}/{booking_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print("\n[성공] 예약 상세 정보:")
        print(response.json())
    else:
        print("\n[실패] 예약 상세 조회에 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def update_booking():
    clear_screen()
    print("=== 예약 정보 수정 ===")

    print("\n[예약 목록]")
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        bookings = response.json()
        if len(bookings) == 0:
            print("[경고] 예약 목록이 비어있습니다.")
            return

        for i, booking in enumerate(bookings, 1):
            print(f"{i}. 예약 ID: {booking['id']}, 환자 이름: {booking['patient_name']}, 예약 날짜: {booking['date']}, 예약 시간: {booking['time']}")
        

        try:
            choice = int(input("\n수정할 예약 번호를 선택하세요 (1부터 번호 입력): "))
            if choice < 1 or choice > len(bookings):
                print("\n[경고] 잘못된 번호입니다. 다시 시도하세요.")

        except ValueError:
            print("\n[경고] 잘못된 입력입니다. 번호를 숫자로 입력하세요.")
        
        booking_to_update = bookings[choice - 1] 
        booking_id = booking_to_update['id']
        print(f"\n선택한 예약 ID: {booking_id}")
        print(f"환자 이름: {booking_to_update['patient_name']}")
        print(f"환자 전화번호: {booking_to_update['patient_phone']}")
        print(f"의사 ID: {booking_to_update['doctor_id']}")
        print(f"예약 날짜: {booking_to_update['date']}")
        print(f"예약 시간: {booking_to_update['time']}")
        print(f"상태: {booking_to_update['status']}")

        print("\n수정할 정보를 입력하세요 (변경하지 않으면 엔터를 눌러주세요):")
        
        patient_name = input(f"환자 이름 ({booking_to_update['patient_name']}): ") or booking_to_update['patient_name']
        patient_phone = input(f"환자 전화번호 ({booking_to_update['patient_phone']}): ") or booking_to_update['patient_phone']
        while True:
            try:
                doctor_id = input(f"의사 ID ({booking_to_update['doctor_id']}): ") or booking_to_update['doctor_id']
                doctor_id = int(doctor_id)  # 의사 ID를 숫자로 변환
                break
            except ValueError:
                print("의사 ID는 숫자로 입력해야 합니다.")
        date = input(f"예약 날짜 ({booking_to_update['date']}): ") or booking_to_update['date']
        time = input(f"예약 시간 ({booking_to_update['time']}): ") or booking_to_update['time']
        status = input(f"상태 ({booking_to_update['status']}): ") or booking_to_update['status']
        
        updated_booking_data = {
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "doctor_id": doctor_id,
            "date": date,
            "time": time,
            "status": status
        }

        # PUT 요청으로 수정
        url = f"{BASE_URL}/{booking_id}"
        response = requests.put(url, json=updated_booking_data)
        if response.status_code == 200:
            print("\n[성공] 예약 정보가 수정되었습니다.")
            print(response.json())
        else:
            print("\n[실패] 예약 수정에 실패했습니다.")
            print(response.json())
    else:
        print("\n[실패] 예약 목록을 조회하는데 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def patch_booking():
    clear_screen()
    print("=== 예약 부분 수정 (상태 변경) ===")
    booking_id = int(input("수정할 예약 ID: "))
    status = input("수정할 예약 상태 (confirmed, cancelled, pending): ")
    updates = {"status": status}

    response = requests.patch(f"{BASE_URL}/{booking_id}", json=updates)
    if response.status_code == 200:
        print("\n[성공] 예약 상태가 변경되었습니다.")
        print(response.json())
    else:
        print("\n[실패] 예약 상태 변경에 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def delete_booking():
    clear_screen()
    print("=== 예약 취소 ===")
    while True:
        try:
            booking_id = int(input("취소할 예약 ID: "))
            break
        except ValueError:
            print("잘못된 입력입니다. 예약 ID는 숫자로 입력하세요.")
    url = f"{BASE_URL}/{booking_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("\n[성공] 예약이 취소되었습니다.")
        print(response.json())
    else:
        print("\n[실패] 예약 취소에 실패했습니다.")
        print(response.json())
    
    input("\n계속하려면 엔터를 눌러주세요.")

def show_menu():
    clear_screen()
    print("=== 예약 관리 시스템 ===")
    print("1. 예약 생성")
    print("2. 예약 목록 조회")
    print("3. 특정 예약 상세 조회")
    print("4. 예약 정보 수정")
    print("5. 예약 부분 수정 (상태 변경)")
    print("6. 예약 취소")
    print("7. 종료")
    print("========================")

def run_application():
    while True:
        show_menu()
        choice = input("원하는 기능 번호를 선택하세요: ")

        if choice == '1':
            create_booking()
        elif choice == '2':
            get_bookings()
        elif choice == '3':
            get_booking()
        elif choice == '4':
            update_booking()
        elif choice == '5':
            patch_booking()
        elif choice == '6':
            delete_booking()
        elif choice == '7':
            clear_screen()
            print("프로그램을 종료합니다.")
            break
        else:
            print("[경고] 잘못된 입력입니다. 다시 시도하세요.")
            input("\n계속하려면 엔터를 눌러주세요.")

if __name__ == "__main__":
    run_application()
