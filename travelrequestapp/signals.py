# travelrequestapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Supervisor  # Use absolute import here

@receiver(post_migrate)
def create_default_supervisors(sender, **kwargs):
    if sender.name == 'travelrequestapp':
        supervisors = [
            {"name": "Marcus Anthony", "job_title": "SR PROGRAM DIRECTOR", "email": "marcus.anthony@rutgers.edu", "supervisor": True},
            {"name": "Meril Antony", "job_title": "POST DOCTORAL ASSOC", "email": "ma1235@newark.rutgers.edu", "supervisor": False},
            {"name": "Vandeen Campbell", "job_title": "ASST RESEARCH PROFESSOR CAL YR", "email": "vandeen.campbell@rutgers.edu", "supervisor": True},
            {"name": "Claudia M. Castillo-Lavergne", "job_title": "POST DOCTORAL ASSOC", "email": "claudia.castillo@rutgers.edu", "supervisor": False},
            {"name": "Danielle Cohen", "job_title": "SR PROGRAM COORDINATOR", "email": "dlcohen@newark.rutgers.edu", "supervisor": False},
            {"name": "Nya-Brielle Earrusso", "job_title": "PROGRAM COORDINATOR I", "email": "ne162@newark.rutgers.edu", "supervisor": False},
            {"name": "Nakeefa C. Garay", "job_title": "SR PROGRAM DIRECTOR", "email": "nbernard@newark.rutgers.edu", "supervisor": False},
            {"name": "Marquise Guzman", "job_title": "SR PROGRAM DIRECTOR", "email": "mig36@newark.rutgers.edu", "supervisor": True},
            {"name": "Robyn Ince", "job_title": "ASST PROF PRF PRAC CY (INEL)", "email": "ri131@newark.rutgers.edu", "supervisor": True},
            {"name": "Amanda Nadine Jaeger", "job_title": "RESEARCH ANALYST", "email": "anj57@newark.rutgers.edu", "supervisor": False},
            {"name": "Alyssa B. King", "job_title": "BUSINESS ASST II", "email": "alyssa.bking@rutgers.edu", "supervisor": False},
            {"name": "Ashaki D. Larkins", "job_title": "MANAGER SPVR", "email": "adl125@newark.rutgers.edu", "supervisor": True},
            {"name": "Bernard Lombardi", "job_title": "RESEARCH SPECIALIST", "email": "bdl48@scarletmail.rutgers.edu", "supervisor": False},
            {"name": "Carlos Jordan Oquendo", "job_title": "PROGRAM COORDINATOR I", "email": "cjo98@newark.rutgers.edu", "supervisor": False},
            {"name": "Erin Santana", "job_title": "POST DOCTORAL ASSOC", "email": "erin.r.santana@rutgers.edu", "supervisor": False},
            {"name": "Kimaada Sills", "job_title": "ASSOC DIRECTOR SPVR", "email": "kimaada@rutgers.edu", "supervisor": True},
            {"name": "Ahmad A. Watson", "job_title": "PROGRAM COORDINATOR I", "email": "ahmad.watson@rutgers.edu", "supervisor": False},
            {"name": "Irene A Welch", "job_title": "ADMINISTRATIVE ASSISTANT", "email": "irenew@rutgers.edu", "supervisor": False},
            {"name": "Charles Payne", "job_title": "DISTINGUISHED PROFESSOR CY", "email": "cp840@newark.rutgers.edu", "supervisor": True},
        ]

        for supervisor_data in supervisors:
            Supervisor.objects.get_or_create(**supervisor_data)
