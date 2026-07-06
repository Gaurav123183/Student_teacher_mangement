from dotenv import load_dotenv
import os
import pymysql
import json
# from .services import DatabaseService
load_dotenv()


##AI connections
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


##start
class DatabaseService:

    @staticmethod
    def get_connection():

        return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        )
    

class Student:
   def signup_user(self, full_name, email, phone, password, role):
    con = DatabaseService.get_connection()
    print("connected successfully")

    curs = con.cursor()
    curs.execute(
        """
        INSERT INTO users
        (full_name, email, password, role, phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (full_name, email, password, role, phone)
    )
    con.commit()         
    curs.close()
    con.close()
    return True
   
   def login_authentication(self, email, password):
    con = DatabaseService.get_connection()
    curs = con.cursor()
    curs.execute(
        """
        SELECT *
        FROM users
        WHERE email=%s AND password=%s
        """,
        (email, password)
    )

    user = curs.fetchone()

    curs.close()
    con.close()

    return user
   ## it take user id 
   def get_user_profile(self, user_id):
    con = DatabaseService.get_connection()
    curs = con.cursor()

    curs.execute(
        """
        SELECT *
        FROM users
        WHERE user_id=%s
        """,
        (user_id,)
    )

    user = curs.fetchone()

    curs.close()
    con.close()

    return user
   
   
   def get_student_profile(self, user_id):
    con = DatabaseService.get_connection()
    curs = con.cursor()

    curs.execute(
        """
        SELECT * FROM students
        WHERE user_id=%s
        """,
        (user_id,)
    )

    student = curs.fetchone()

    curs.close()
    con.close()

    return student
   

##it will insert or update only student table which having these attribute ..... it will not update users table->name,email,phone
   def save_student_profile(
    self,
    user_id,
    enrollment_no,
    course,
    semester,
    section,
    college_name,
    joining_date
    ):
     con = DatabaseService.get_connection()
     curs = con.cursor()
     curs.execute(
    """
    SELECT * FROM students
    WHERE user_id=%s
    """,
    (user_id,)
       )

     student = curs.fetchone()
     print("Student Record:", student)
     print("Session User ID:", user_id)
     if student:
      print("UPDATE RUNNING")

      curs.execute(
        """
        UPDATE students
        SET enrollment_no=%s,
            course=%s,
            semester=%s,
            section=%s,
            college_name=%s,
            joining_date=%s
        WHERE user_id=%s
        """,
        (
            enrollment_no,
            course,
            semester,
            section,
            college_name,
            joining_date,
            user_id
        )
      )
     else:
        print("INSERT RUNNING")

        curs.execute(
        """
        INSERT INTO students
        (
            user_id,
            enrollment_no,
            course,
            semester,
            section,
            college_name,
            joining_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            enrollment_no,
            course,
            semester,
            section,
            college_name,
            joining_date
        )
    )
     con.commit()
     
     ###after that user will edit or update here
   def update_user_profile(
    self,
    user_id,
    full_name,
    email,
    phone
):

    con = DatabaseService.get_connection()
    curs = con.cursor()

    curs.execute(
        """
        UPDATE users
        SET full_name=%s,
            email=%s,
            phone=%s
        WHERE user_id=%s
        """,
        (
            full_name,
            email,
            phone,
            user_id
        )
    )

    con.commit()
    curs.close()
    con.close()

  ##for image 
   def update_profile_image(self, user_id, image_path):

     con = DatabaseService.get_connection()
     curs = con.cursor()

     curs.execute(
        """
        UPDATE users
        SET profile_image=%s
        WHERE user_id=%s
        """,
        (image_path, user_id)
    )

     con.commit()

     curs.close()
     con.close()




   def evaluate_code_image(self, image_path):

    uploaded_file = client.files.upload(
        file=image_path
    )

    prompt = """
You are an expert software engineer and programming mentor.

The uploaded image contains source code written by a student.

First extract the code exactly as written.

Then return ONLY VALID JSON.

Rules:

1. Do not write any explanation outside JSON.
2. Do not wrap JSON inside ```json blocks.
3. Return valid JSON only.

Return exactly this structure:

{
    "language":"",
    "score":0,

    "score_breakdown":{
        "code_quality":0,
        "readability":0,
        "optimization":0,
        "security":0,
        "maintainability":0,
        "best_practices":0
    },

    "topics":[
        ""
    ],

    "issues":[
        {
            "line":"",
            "problem":"",
            "reason":"",
            "fix":"",
            "example":""
        }
    ],

    "extracted_code":"",

    "corrected_code":"",

    "summary":""
}

Important:

- Preserve student's logic.
- Do NOT generate a completely new solution.
- Fix only mistakes.
- Correct syntax errors.
- Keep explanations short.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded_file,
            prompt
        ]
    )
    print(response.text)

    text = response.text

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)