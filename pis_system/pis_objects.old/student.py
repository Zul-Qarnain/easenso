from pis_system.models import Student, StudentSubjects, StudentGrade, StudentSection

class StudentObj(object):
    
    def __init__(self):
        self.stud_id = 0
        self.stud_grades = []

    '''
    def __init__(self, stud_id):
        self.stud_id = stud_id
        self.stud_grades = []
    '''
 
    def getGrades(self, sch_year):
        try:
#            stud_subj = StudentSubjects.objects.filter(student=self.stud_id)
            stud_subj = StudentSubjects.objects.raw("SELECT * FROM pis_system_studentsubjects WHERE student_id=%s AND school_year=%s", [self.stud_id, sch_year])
            for subj in stud_subj:
                grades = StudentGrade.objects.filter(student_subject=subj.id)
                subj_grade = {}
                subj_grade['subject'] = subj.subject.title
                for grade in grades:
                    if grade.grading_period==1:
                        subj_grade['1st'] = grade.grade
                    elif grade.grading_period==2:
                        subj_grade['2nd'] = grade.grade
                    elif grade.grading_period==3:
                        subj_grade['3rd'] = grade.grade
                    elif grade.grading_period==4:
                        subj_grade['4th'] = grade.grade
                    else:
                        subj_grade['final'] = grade.grade
                    self.stud_grades.append(subj_grade)

            return self.stud_grades    
        except Exception:
            return 0
    
    def getInfo(self):
        try:
            student = Student.objects.get(studentID=self.stud_id)
            return student
        except Student.DoesNotExist:
            return 0
            

    def getSYInvolved(self):
        sy = StudentSection.objects.raw("SELECT id,school_year FROM pis_system_studentsubjects WHERE student_id=%s GROUP BY id,school_year", [self.stud_id])#school year list
        return sy
    
    def searchStud(self, search_text, search_opt):
        '''
        precondition: search_text->  search parameter student retrieval
                      search_opt-> search option for searching student, could
                                   be by id, firstname or lastname
        postcondition: returns a list of student dictionary
        '''
        students = {}
        try:
            if search_opt=='stud_id':
                students = Student.objects.filter(studentID__contains=search_text)
            elif search_opt=='first_name':
                students = Student.objects.filter(firstname__contains=search_text)
            elif search_opt=='last_name':
                students = Student.objects.filter(lastname__contains=search_text)
            return students
        except Student.DoesNotExist:
            return null


    #def addStudent(self, stud_info):
        
        

    def __del__(self):
        del self.stud_grades
        del self.stud_id
        
