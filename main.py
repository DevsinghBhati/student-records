import json
import os

class Student:
    def __init__(self, student_id, roll_no, name, age):
        self.student_id = student_id
        self.roll_no = roll_no
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            "id": self.student_id,
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age
        }

class StudentManager:
    def __init__(self, filepath='students.json'):
        self.filepath = filepath
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_students(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.students, file, indent=4)

    def id_or_roll_exists(self, student_id, roll_no):
        for student in self.students:
            if student['id'] == student_id or student['roll_no'] == roll_no:
                return True
        return False

    def find_by_id(self, student_id):
        for student in self.students:
            if student['id'] == student_id:
                return student
        return None

    def add_student(self, student):
        if self.id_or_roll_exists(student.student_id, student.roll_no):
            print(" Student ID or Roll Number already exists! Cannot add.")
            return
        self.students.append(student.to_dict())
        self.save_students()
        print(" Student added successfully.")

    def update_student(self, student_id, updates):
        for student in self.students:
            if student["id"] == student_id:
                if "roll_no" in updates:
                    if any(s['roll_no'] == updates["roll_no"] and s["id"] != student_id for s in self.students):
                        print(" This Roll Number already exists with another student.")
                        return
                student.update(updates)
                self.save_students()
                print(" Student updated successfully.")
                return
        print(" Student ID not found. Cannot update.")

    def delete_student(self, student_id):
        for i, student in enumerate(self.students):
            if student["id"] == student_id:
                print(f"deleting..... \nstudent: {self.students[i]}")
                del self.students[i]
                self.save_students()
                print(" Student deleted successfully.")
                return
        print(" Student ID not found. Cannot delete.")

    def show_students(self):
        if not self.students:
            print(" No students found.")
        for student in self.students:
            print(
                f"ID: {student['id']}, Roll No: {student['roll_no']}, "
                f"Name: {student['name']}, Age: {student['age']}"
            )

def main():
    manager = StudentManager()

    while True:
        print("\n Student Management System")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Show Students")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            sid = input("Enter Student ID: ").strip()
            roll_no = input("Enter Roll Number: ").strip()
            name = input("Enter Name: ").strip()
            age = input("Enter Age: ").strip()

            if not all([sid, roll_no, name, age]):
                print(" Cannot add student. All fields are required.")
                continue

            if manager.id_or_roll_exists(sid, roll_no):
                print(" ID or Roll Number already exists. Cannot add.")
                continue

            student = Student(sid, roll_no, name, age)
            manager.add_student(student)

        elif choice == '2':
            sid = input("Enter Student ID to update: ").strip()
            student = manager.find_by_id(sid)
            if not student:
                print(" This ID does not exist.")
                continue

            print(" Leave any field blank to skip updating it.")
            new_roll = input("New Roll Number (press Enter to skip): ").strip()
            new_name = input("New Name (press Enter to skip): ").strip()
            new_age = input("New Age (press Enter to skip): ").strip()

            updates = {}
            if new_roll: updates["roll_no"] = new_roll
            if new_name: updates["name"] = new_name
            if new_age: updates["age"] = new_age

            if updates:
                manager.update_student(sid, updates)
            else:
                print(" No changes made.")

        elif choice == '3':
            sid = input("Enter Student ID to delete: ").strip()
            manager.delete_student(sid)

        elif choice == '4':
            manager.show_students()

        elif choice == '5':
            print(" Exiting...")
            break

        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    main()
