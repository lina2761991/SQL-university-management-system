import mysql.connector as mysql
from prettytable import PrettyTable



#variables
host = "localhost"
user = "root"
password = ""
database="university2"


#connecting to mysql
try:
    db = mysql.connect(host=host, user=user,password=password,database=database)
    print("connected successfully")
except Exception as e:
    print(e)
    print("Failed to connect") 
command_handler= db.cursor(buffered=True)

##### admin session ################
def admin_session(): 
    while 1:
        print("")
        print("Admin Menu")
        print("1. Manage Classes") # DONE !!!
        print("2. Manage Subjects") # DONE !!!
        print("3. Manage Students") # DONE !!!
        print("4. Manage Teachers") # DONE !!!
        print("5. Logout") 
        user_option = input(str("Option : "))


       #####################     Manage Classes ############################################

        if user_option == "1":

            print("1. View List of classes")
            print("2. Add A New Class")
            print("3. Update A class")
            print("4. Delete A class")
            user_option2= input(str("Option : "))


            if user_option2 == "1":
               def ViewClasses():
                    command_handler.execute("Select className from class")
                    records = command_handler.fetchall()
                    myTab = PrettyTable(['Class Name'])
                    for record in records:
                        l = list(record)
                        myTab.add_row(l)
                    print(myTab)
               ViewClasses()    
                    
               
            elif user_option2 == "2":
                c = input(str("Class Name : ")) 
                command_handler.execute("INSERT INTO class (className) VALUES (%s)",(c,))
                db.commit()
                print(c+" has been added !")   
                ViewClasses() 

            elif user_option2 == "3": 
                print("")
                print("Update Existing Class:")
                c1 = input(str("Old Class Name : "))  
                c2 = input(str("New Class Name : "))  
                command_handler.execute("UPDATE class set className = %s WHERE className  = %s",(c2,c1))
                db.commit()
                print(c1+" has been updated to "+c2 +"!")
                ViewClasses() 


            elif user_option2 == "4":
                print("")
                print("Delete Existing Class:")
                c = input(str("Class Name : "))  
                command_handler.execute("DELETE FROM students WHERE StudentClass = (select classId FROM class where className = %s)",(c,))
                db.commit()
                command_handler.execute("DELETE FROM class WHERE className = %s",(c,))
                db.commit()
                print(c+" has been deleted !")
                


    #####################     Manage Students   ############################################



        elif user_option == "3":

            print("1. View List of students") #search for student by letters
            print("2. Add A New Student")
            print("3. Update A Student")
            print("4. Delete A Student")
            user_option2= input(str("Option : "))
                ######     View  Students   ####

            if user_option2 == "1":
               
               def ViewStudents():
                    command_handler.execute("SELECT  fname , lname, email, phone, adresse, EnrollementDate, DateOfBirth, className FROM users inner join students on users.UserID = students.UserID  inner join class on students.StudentClass = class.classID WHERE users.UserTypeID = 1 order by class.classID")
                    records = command_handler.fetchall()
                    myTab = PrettyTable(['First Name', 'Last Name', 'Email', 'Phone','Adress', 'Enrollement Date', 'Date Of Birth', 'Class'])
                    for record in records:
                         l = list(record)
                         myTab.add_row(l)
                    print(myTab)

               ViewStudents()    


                ######     Add a New  Student  ####
            if user_option2 == "2":
                               
                c1 = input(str("Student First Name : ")) 
                c2 = input(str("Student LAst Name : "))
                c3 = input(str("Email : ")) 
                c4 = input(str("Phone : ")) 
                c5 = input(str("Password : ")) 
                c6 = input(str("Adresse : ")) 
                c7 = input(str("Enrollement Date (yyyy-mm-dd) : "))
                c8 = input(str("Date Of Birth (yyyy-mm-dd) : ")) 
                c9 = input(str("Class : "))
                command_handler.execute("SELECT classID from Class where classname = '"+c9+"'")
                stdclass =  command_handler.fetchall()[0][0]
                command_handler.execute("SELECT max(UserID) from users")
                id = command_handler.fetchall()[0][0]+1
                sid= str(id)
                         #added to the users
                command_handler.execute("INSERT INTO USERS (UserID, UserTypeID, fname, lname, email, phone, password, adresse)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(id,1,c1,c2,c3,c4,c5,c6))
                db.commit()          
                         ### then we should add to students
                command_handler.execute("INSERT INTO students (UserID, UserTypeID, EnrollementDate, DateOfBirth, StudentClass)  VALUES (%s,%s,%s,%s,%s)",(sid, '1',c7 ,c8 , stdclass))
                db.commit()
                print("Student Added Successfully !")
                print("The New Students List :")
                ViewStudents() 
          
               ######     Delete A Student   ####
            if user_option2 == "4":
                 command_handler.execute("SELECT  fname , lname, email, phone, adresse, EnrollementDate, DateOfBirth, className FROM users inner join students on users.UserID = students.UserID  inner join class on students.StudentClass = class.classID WHERE users.UserTypeID = 1 order by class.classID")
                 records = command_handler.fetchall()
                 myTab = PrettyTable(['First Name', 'Last Name', 'Email', 'Phone','Adress', 'Enrollement Date', 'Date Of Birth', 'Class'])
                 for record in records:
                    l = list(record)
                    myTab.add_row(l)
                 print(myTab)
                 e = input(str("Select the student email : ")) 
                 command_handler.execute("Select UserID FROM users WHERE  email = %s",(e,)) 

                 stide = command_handler.fetchall()[0][0]
                 print(stide)
                 ## delete from students
                 command_handler.execute("DELETE FROM students WHERE UserID = %s",(stide,))
                 db.commit()
                 #delete from users
                 command_handler.execute("DELETE FROM users WHERE  email= %s",(e,))
                 db.commit()
                 if command_handler.rowcount < 1 :
                    print("student not found") 
                 else:
                    print("student has been deleted !")
                    print("The New Students List :")
                    ViewStudents() 
                      ######     Update a  Student   ####
            if user_option2 == "3":
                               
                    o1 = input(str("Student First Name : ")) 
                    o2 = input(str("Student LAst Name : "))
            
                    c1 = input(str("New First Name : ")) 
                    c2 = input(str("New LAst Name : "))
                    c3 = input(str("New Email : ")) 
                    c4 = input(str("New Phone : ")) 
                    c5 = input(str("New Adresse : ")) 
                    c6 = input(str("New Enrollement Date (yyyy-mm-dd) : "))
                    c7 = input(str("New Date Of Birth (yyyy-mm-dd) : ")) 
                    c8 = input(str("New Class : "))
                    
                    command_handler.execute("UPDATE users inner join students on users.userID = students.UserId SET users.fname = %s ,  users.lname = %s,  users.email = %s, users.phone = %s, users.adresse = %s , students.EnrollementDate = %s , students.DateOfBirth = %s , students.StudentClass = (select classId FROM class where className = %s) WHERE users.fname =%s and users.lname = %s",(c1,c2,c3,c4,c5,c6,c7,c8,o1,o2))
                    db.commit()
                    print("student updated")
                    print("The New Students List :")
                    ViewStudents() 


                    #############################################################      Manage Subjects       #############################################################################################

        elif user_option == "2":

            print("1. View List of Subjects")
            print("2. Add A New Subject")
            print("3. Update A Subject")
            print("4. Delete A Subject")
            user_option2= input(str("Option : "))


            if user_option2 == "1":
               
               def ViewSubjects():
                    command_handler.execute("Select subjectName, subjectCoef from subject")
                    records = command_handler.fetchall()
                    myTab = PrettyTable(['Subject Name', 'Subject Coefficient'])
                    for record in records:
                         l = list(record)
                         myTab.add_row(l)
                    print(myTab)

               ViewSubjects()
               
            elif user_option2 == "2":
                c = input(str("Subject Name : ")) 
                d = input(str("Subject Coefficient : ")) 
                command_handler.execute("INSERT INTO subject (subjectName, subjectCoef) VALUES (%s,%s)",(c,d))
                db.commit()
                print(c+" has been added !")   
                #ViewSubjects()

            elif user_option2 == "3": 
                print("")
                print("Update Existing Subject:")
                c1 = input(str("Old Subject Name : "))  
                c2 = input(str("New Subject Name : "))  
                c3 = int(input(str("New Subject Coefficient : "))) 
                command_handler.execute("UPDATE subject set subjectName = %s , subjectCoef = %s WHERE subjectName  = %s",(c2,c3,c1))
                db.commit()
                print(c1+" has been updated to "+c2)
                #ViewSubjects()


            elif user_option2 == "4":
                print("")
                print("Delete Existing Subject:")
                c = input(str("Subject Name : "))  
                command_handler.execute("DELETE FROM teachers WHERE subject = (select subjectID FROM subject where subjectName = %s)",(c,))
                db.commit()
                command_handler.execute("DELETE FROM exam WHERE subjectID = (select subjectID FROM subject where subjectName = %s)",(c,))
                db.commit()
                command_handler.execute("DELETE FROM subject WHERE subjectName = %s",(c,))
                db.commit()
                print(c+" has been deleted ")
               

                 #####################     Manage Teachers   ############################################



        elif user_option == "4":

            print("1. View List of Teachers")
            print("2. Add A New Teacher")
            print("3. Update A Teacher")
            print("4. Delete A Teacher")
            user_option2 = input(str("Option : "))
                ######     View  Teachers   ####

            if user_option2 == "1":
               
               def ViewTeachers():
                    global myTab
                    command_handler.execute("SELECT  fname , lname, email, phone, adresse, HireDate, subjectName FROM users inner join teachers on users.UserID = teachers.UserID  inner join subject on teachers.subject = subject.subjectID WHERE users.UserTypeID = 2")
                    records = command_handler.fetchall()
                    myTab = PrettyTable(['First Name', 'Last Name', 'Email', 'Phone','Adress', 'Hire Date', 'Subject'])
                    for record in records:
                         l = list(record)
                         myTab.add_row(l)
                    print(myTab)

               ViewTeachers()    


                ######     Add a New  Teacher  ####
            if user_option2 == "2":
                               
                c1 = input(str("Teacher First Name : ")) 
                c2 = input(str("Teacher LAst Name : "))
                c3 = input(str("Email : ")) 
                c4 = input(str("Phone : ")) 
                c5 = input(str("Password : ")) 
                c6 = input(str("Adresse : ")) 
                c7 = input(str("Hire Date (yyyy-mm-dd) : "))
                c8 = input(str("Subject : "))
                command_handler.execute("SELECT subjectID from subject where subjectName = '"+c8+"'")
                stdclass =  command_handler.fetchall()[0][0]
                command_handler.execute("SELECT max(UserID) from users")
                id = command_handler.fetchall()[0][0]+1
                sid= str(id)
                         #added to the users
                command_handler.execute("INSERT INTO USERS (UserID, UserTypeID, fname, lname, email, phone, password, adresse)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(id,2,c1,c2,c3,c4,c5,c6))
                db.commit()          
                         ### then we should add to teachers
                command_handler.execute("INSERT INTO teachers (UserID, UserTypeID, HireDate,subject )  VALUES (%s,%s,%s,%s)",(sid, '2',c7 ,stdclass))
                db.commit()
                print("Teacher Added Successfully !")
                print("The New Teachers List :")
                #ViewTeachers()
               ######     Delete A Teacher   ####
            if user_option2 == "4":
                 ViewTeachers() 
                 
                 e = input(str("Select the teacher email : ")) 
                 command_handler.execute("Select UserID FROM users WHERE  email = %s",(e,)) 

                 stide = command_handler.fetchall()[0][0]
                 print(stide)
                 ## delete from teachers
                 command_handler.execute("DELETE FROM teachers WHERE UserID = %s",(stide,))
                 db.commit()
                 #delete from users
                 command_handler.execute("DELETE FROM users WHERE  email= %s",(e,))
                 db.commit()
                 print("teacher has been deleted !")
                 print("The New Teachers List :")
                 ViewTeachers() 
                      ######     Update a  Teacher   ####
            if user_option2 == "3":
                
                               
                o1 = input(str("Teacher First Name : ")) 
                o2 = input(str("Teacher LAst Name : "))
            
                c1 = input(str("New First Name : ")) 
                c2 = input(str("New LAst Name : "))
                c3 = input(str("New Email : ")) 
                c4 = input(str("New Phone : ")) 
                c5 = input(str("New Adresse : ")) 
                c6 = input(str("New Hire Date (yyyy-mm-dd) : ")) 
                c7 = input(str("New Subject : "))
                    
                command_handler.execute("UPDATE users inner join teachers on users.userID = teachers.UserID SET users.fname = %s ,  users.lname = %s,  users.email = %s, users.phone = %s, users.adresse = %s , Teachers.HireDate = %s , teachers.subject = (select subjectId FROM subject where subjectName = %s) WHERE users.fname =%s and users.lname = %s",(c1,c2,c3,c4,c5,c6,c7,o1,o2))
                db.commit()
                print("teacher updated")
                
                
                ########################################################## LOG OUT  #################################################################################################################################
                                   

        elif user_option == "5":
            break
        else:
            print("no valid option  ! ")

######  auth admin    ###############
def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin" :
        if password == "admin":
            admin_session()
        else:
            print("Incorrect password !")
    else:
        print("Login details not recognised !")

def teacher_session(username,password):
    while 1:
        print("")
        print("Teacher Menu")
        print("1. View Attendance")
        print("2. Mark Class Attendance")
        print("3. Manage Exams")
        print("4. change password")
        print("5. Logout") 

        user_option = input(str("Option : "))
        #######################  View Attendance    ###############
        if user_option == "1":
             x = input(str("Type The Date (yyyy-mm-dd): "))
             y = input(str("Type The Class Name : "))
             print(" The attendance of "+ y +" at "+ x)
             command_handler.execute("select subject.subjectID from  teachers inner join subject on teachers.subject = subject.subjectID inner join users on users.UserID = teachers.UserID where users.fname =%s ",(username,))
             records =  command_handler.fetchall()
             z = records[0][0]
        
             command_handler.execute("Select users.fname, users.lname ,attendance.status from attendance inner join class on attendance.classID = class.classID inner join users on users.UserID = attendance.UserID  where class.className =%s and date = %s and attendance.subject = %s ",(y,x,z))
             records = command_handler.fetchall()
             myTab = PrettyTable(['Student First Name','Student Last Name','Status(Abscent A -- Present P)'])
             for record in records:
                l = list(record)
                myTab.add_row(l)
             print(myTab)


        ####################### Mark Class Attendance    ###############
        elif user_option == "2":
             x = input(str("Type The Date (yyyy-mm-dd): "))
             y = input(str("Type The Class Name : "))
             command_handler.execute("SELECT users.fname,users.lname,users.UserID,class.classID FROM students inner join class on students.StudentClass = class.classID inner join users on users.UserID = students.UserID  WHERE class.className=%s ",(y,))
             records = command_handler.fetchall()

             command_handler.execute("select subject.subjectID from  teachers inner join subject on teachers.subject = subject.subjectID inner join users on users.UserID = teachers.UserID where users.fname =%s ",(username,))
             records2 =  command_handler.fetchall()
             z = records2[0][0]
             for record in records:
                l = list(record)
                fname=l[0]
                lname=l[1]
                userId=l[2]
                classId=l[3]
                status = input(str("Status for " +fname+" "+ lname+ " P/A : "))
                query_vals = (x,status,classId,userId,z)
                command_handler.execute("INSERT INTO attendance (date,status,classID,UserID,subject) VALUES (%s,%s,%s,%s,%s)",query_vals)
                db.commit()
                print(fname+" "+ lname+  " Marked as "+status)
           ####################### Manage exams   ###############
        elif user_option == "3":
            print("")
            print("1. View Exams Marks")
            print("2. Add Exams Marks")
            print("3. Logout") 

            user_option2 = input(str("Option : "))
            if user_option2 == "1":
                 x = input(str("Class Name: "))
                 a = ()
                 b = ()
                 command_handler.execute("Select exam.studentID ,Subject.subjectName, exam.NoteCC, exam.NoteExamen,ROUND((exam.NoteCC * 0.3 + exam.NoteExamen*0.7),2) as Moyenne from exam inner join subject on subject.subjectID = exam.subjectID inner join teachers on teachers.subject = subject.subjectID inner join users on users.UserID = teachers.UserID where users.fname =  %s and users.password =%s and exam.studentId IN (select students.UserID from students inner join class on students.StudentClass = class.classID where class.ClassName =%s)",(username,password,x))
                 records = command_handler.fetchall()

                 myTab = PrettyTable(['Student ID','Subject Name','CC Mark','Exam Mark','Average'])
                 for record in records:
                    l = list(record)
                    myTab.add_row(l)
                 #print(myTab)

                 ######
                 for record in records:
                     a = a +(record[0],)
                 myTab2 = PrettyTable(['Student First Name','Student Last Name',])
                 for x in a:
                     command_handler.execute("select users.fname, users.lname from users where UserID=%s",(x,))
                     records1 =command_handler.fetchall()
             
                     for record in records1:
                        l = list(record)
                        myTab2.add_row(l)
   
                 z = PrettyTable()
                 z_rows = []
                 counter = 0
                 for i in myTab2.rows:
                    i.extend(myTab.rows[counter])
                    counter += 1
                    z_rows.append(i)

                 field = []
                 field.extend(myTab2.field_names)
                 field.extend(myTab.field_names)

                 z.field_names = field
                 z.add_rows(z_rows)
                 # print("####################### tab 3 #############################")
                 print(z)
            
            elif user_option2 == "2":### inserting the exams marks
                   
                
                 y = input(str("Type The Class Name : "))
                 # displaying the list of students in the class
                 command_handler.execute("SELECT users.fname,users.lname,users.UserID,class.classID FROM students inner join class on students.StudentClass = class.classID inner join users on users.UserID = students.UserID  WHERE class.className=%s ",(y,))
                 records = command_handler.fetchall()

                 #displaying the subject ID   
                 command_handler.execute("select subject.subjectID from  teachers inner join subject on teachers.subject = subject.subjectID inner join users on users.UserID = teachers.UserID where users.fname =%s ",(username,))
                 records2 =  command_handler.fetchall()


                 z = records2[0][0]
                 for record in records:
                    l = list(record)
                    fname=l[0]
                    lname=l[1]
                    userId=l[2]
                    classId=l[3]
                    notecc = input(str("CC Mark for "+ fname+ " "+ lname +":"))
                    noteexam = input(str("Exam Mark "+ fname+ " "+ lname +": "))
             
                    query_vals = (userId,z,notecc,noteexam)

                    command_handler.execute("INSERT INTO exam (StudentID,subjectID,NoteCC,NoteExamen) VALUES (%s,%s,%s,%s)",query_vals)
                    db.commit()
                    print("exams marked")
            elif user_option2 == "3":
                break;   

            
        elif user_option == "4":
            x = input(str("The Old Password : "))
            o = input(str("The New Password : "))
            command_handler.execute("UPDATE users SET users.password = %s  WHERE users.fname =%s ",(o,username))
            db.commit()
            print("Password Updated !")
            

        elif user_option == "5":
            break
        else:
            print("No valid option was selected")

def student_session(username,password):
    while 1:
        print("")
        print("Student's Menu")
        print("1. View His Attendance") #Done !!
        print("2. View His Exams Marks")# Done !!
        print("3. Download Exams Marks") # to do
        print("4. Change password") #Done !!
        print("5. Logout") #Done !!
        user_option = input(str("Option : "))
         ###########################  View His Attendance   #####################################
        if user_option == "1":
            print("Displaying Register")
            #username1 = (str(username),)

            command_handler.execute("select attendance.date, subject.subjectName, attendance.status from attendance inner join users on attendance.UserID=users.UserID inner join subject on attendance.subject = subject.subjectID where users.fname= %s",(username,))
            records1 = command_handler.fetchall()
            myTab1 = PrettyTable(['Attendance Date','Subject Name','Status(P for Present/A for Abscent)'])
            for record in records1:
                l = list(record)
                myTab1.add_row(l)
            print(myTab1)

         ###########################  View His Exams Marks   #####################################
        elif user_option == "2":
            print("Exams Marks")
            #username = (str(username),)
            command_handler.execute("select subject.subjectName, subject.subjectCoef,exam.NoteCC,exam.NoteExamen, (exam.NoteCC*0.3+exam.NoteExamen*0.7) as moyenne from exam inner join subject on exam.subjectID = subject.subjectID inner join users on exam.studentID = users.UserID where users.fname= %s",(username,))
            records2 = command_handler.fetchall()
            print("records")
            #print(records2)
            myTab2 = PrettyTable(['Subject Name','Subject Coefficient','CC Mark','Exam Mark', 'Subject Mark'])
            for record in records2:
                l = list(record)
                myTab2.add_row(l)
            print(myTab2)
         ###########################  Download Exams Marks   #####################################

        elif user_option == "3":
             print("Download Register")
             #username = (str(username),)
             command_handler.execute("select subject.subjectName, subject.subjectCoef,exam.NoteCC,exam.NoteExamen, (exam.NoteCC*0.3+exam.NoteExamen*0.7) as moyenne from exam inner join subject on exam.subjectID = subject.subjectID inner join users on exam.studentID = users.UserID where users.fname= %s",(username,))
             records = command_handler.fetchall()
             for record in records:
                 with open("C:/Users/Lina Ben Salem/Desktop/Records/Exams.txt", "w") as f:
                      f.write("subject Name, subject Coef ,CC Mark, Exam Mark ,Average"+"\n")
                      r = str(records)
                      r.replace("["," ")
                      r.replace("]"," ")
                      r.replace("("," ")
                      r.replace(")"," ")
                      r.replace("'"," ")
                      f.write(r+"\n")
                 f.close()
             print("All records saved !")
           ###########################   change password    ##################################### 
        elif user_option == "4":
            x = input(str("The Old Password : "))
            o = input(str("The New Password : "))
            command_handler.execute("UPDATE users SET users.password = %s  WHERE users.fname =%s ",(o,username))
            db.commit()
            print("Password Updated !")    
             ###########################    Log Out  #####################################
        elif user_option == "5":
            break
        else:
            print("No Valid option was selected")
        
            


def auth_teacher():
    print("")
    print("Teacher Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals =(username, password)
    command_handler.execute("SELECT * FROM users WHERE fname = %s AND password = %s AND UserTypeID = 2",query_vals)
    if command_handler.rowcount <=0:
        print("Login not recognized")
    else:
        teacher_session(username, password)


def auth_student():
    #import pdb; pdb.set_trace()
    print("")
    print("Student Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals =(username, password)
    command_handler.execute("SELECT * FROM users WHERE fname = %s AND password = %s AND  UserTypeID = 1",query_vals)
    #username=  command_handler.fetchone()
    if command_handler.rowcount <= 0:
        print("Invalid Login details")
    else:
        student_session(username,password)

def main():
    while 1:
        print("Welcome to Pristini University !")
        print("")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        else:
            print("Warning ! No valid option was selected !")


main()