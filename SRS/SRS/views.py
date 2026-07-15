from urllib import request


from django.shortcuts import render,redirect
import mysql.connector 


def insertdata(name, roll, dept, semester, email, phn, adress):
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host="database-2.ctow2msws1md.us-east-2.rds.amazonaws.com",
            user="admin",
            password="12345678",
            database="mytestdb"
        )

        cursor = conn.cursor()

        sql = """
        INSERT INTO student
        (name, roll, department, semester, email, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (name, roll, dept, semester, email, phn, adress)

        cursor.execute(sql, values)
        conn.commit()

        return True

    except Exception as e:
        if conn:
            conn.rollback()
        return e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def register(request):
    name = request.POST.get('name')
    roll = request.POST.get('roll')
    department = request.POST.get('department')
    semester = request.POST.get('semester')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')

    if name and roll and department and semester and email:
        insertdata(name, roll, department, semester, email, phone, address)

        return redirect('home')   # Go back to home after saving

    return render(request, 'register.html')




def home(request):
    conn = mysql.connector.connect(
        host="database-2.ctow2msws1md.us-east-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="mytestdb"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student ORDER BY id DESC LIMIT 1")
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render(request, "home.html", {"student": student})



def student_list(request):
    conn = mysql.connector.connect(
        host="database-2.ctow2msws1md.us-east-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="mytestdb"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student ORDER BY id DESC")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, "student_list.html", {"students": students})

from django.shortcuts import render, redirect
import mysql.connector

def update(request, id):

    conn = mysql.connector.connect(
        host="database-2.ctow2msws1md.us-east-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="mytestdb"
    )

    cursor = conn.cursor()

    if request.method == "POST":

        name = request.POST.get("name")
        roll = request.POST.get("roll")
        department = request.POST.get("department")
        semester = request.POST.get("semester")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        sql = """
        UPDATE student
        SET
            name=%s,
            roll=%s,
            department=%s,
            semester=%s,
            email=%s,
            phone=%s,
            address=%s
        WHERE id=%s
        """

        values = (
            name,
            roll,
            department,
            semester,
            email,
            phone,
            address,
            id
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("student_list")

    # Load existing student details
    cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render(request, "update.html", {"student": student})


def delete(request, id):

    conn = mysql.connector.connect(
        host="database-2.ctow2msws1md.us-east-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="mytestdb"
    )

    cursor = conn.cursor()

    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("student_list")