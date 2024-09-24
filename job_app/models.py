from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(
        upload_to='category_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    country =models.CharField(max_length=100,unique=False,null=False,blank=False)
    city = models.CharField(max_length=50,unique=True,null=False,blank=False)

    def __str__(self):
        return f"{self.country}, {self.city}"


class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Job(models.Model):
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    CONTRACT = 'CT'
    INTERNSHIP = 'IN'
    REMOTE = 'RM'
    FREELANCE = 'FL'
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time'),
        (CONTRACT, 'Contract'),
        (INTERNSHIP, 'Internship'),
        (REMOTE, 'Remote'),
        (FREELANCE, 'Freelance'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    job_type = models.CharField(
        max_length=2, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    vacancies = models.IntegerField()
    required_knowledge_skills_abilities = models.TextField()
    education_experience = models.TextField()
    min_experience_years = models.IntegerField()  # For filtering based on experience
    job_category = models.ForeignKey(Category, on_delete=models.CASCADE)
     

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"




class Contact(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, verbose_name="Full Name")
    email = models.EmailField(max_length=100, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)

    
    def __str__(self):
        return self.subject
