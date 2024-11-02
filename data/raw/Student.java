import java.util.ArrayList;
import java.util.List;

public class Student {
    private String name;
    private int age;
    private List<Integer> grades;
    private int attendanceDays;

    // Constructor
    public Student(String name, int age) {
        this.name = name;
        this.age = age;
        this.grades = new ArrayList<>();
        this.attendanceDays = 0;
    }

    // Method to add a grade
    public void addGrade(int grade) {
        grades.add(grade);
    }

    // Method to calculate average grade
    public double calculateAverage() {
        if (grades.isEmpty()) return 0.0;
        int total = grades.stream().mapToInt(Integer::intValue).sum();
        return (double) total / grades.size();
    }

    // Method to update attendance
    public void markAttendance() {
        attendanceDays++;
    }

    // Method to display student information
    public void displayInfo() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Average Grade: " + calculateAverage());
        System.out.println("Attendance Days: " + attendanceDays);
    }

    public static void main(String[] args) {
        Student student = new Student("Alice", 20);
        student.addGrade(85);
        student.addGrade(92);
        student.addGrade(78);
        student.markAttendance();
        student.markAttendance();
        student.displayInfo();
    }
}
