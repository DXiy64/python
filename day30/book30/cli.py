from .store import ContactBook

def show_menu():
    print("1. 添加记录")
    print("2. 查看记录")
    print("3. 删除记录")
    print("4. 退出")
    print("5. 月报")


def main():
    book = ContactBook()
    try:
        while True:
            show_menu()
            choice = input("请输入选项：")
            if choice == "1":
                money = input("请输入金额：")
                sort = input("请输入类别：")
                note = input("请输入备注：")
                book.add(money, sort, note)
            elif choice == "2":
                book.show()
            elif choice == "3":
                book.show()
                id = input("请输入要删除的记录ID：")
                book.delete(id)
            elif choice == "4":
                break
            elif choice == "5":
                month = input("请输入月份（YYYY-MM）：")
                count, total = book.month_report(month)
                print(f"{month} 共 {count} 笔，总金额 {total:.2f}")
            else:
                print("无效选项，请重新输入")
    finally:
        book.close()


if __name__ == "__main__":
    main()