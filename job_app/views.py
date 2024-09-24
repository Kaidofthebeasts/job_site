from django.shortcuts import get_object_or_404, render
import operator
from functools import reduce
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from datetime import datetime
from .forms import ApplicationForm, JobForm, CompanyForm, LocationForm, CategoryForm, ContactForm, CustomUserCreationForm
from .models import Company, Location, Category,Job,Application,Contact
from .decorators import staff_required
# Create your views here.





def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


@staff_required
def dashboard(request):
    sort_by = request.GET.get('sort', 'title')  # Default sorting by job title
    filter_by = request.GET.get('filter', '')  # Default no filter

    companies = Company.objects.all()
    jobs = Job.objects.filter(
        Q(title__icontains=filter_by) |
        Q(description__icontains=filter_by) |
        Q(company__name__icontains=filter_by)
    ).order_by(sort_by)
    categories = Category.objects.all()
    applications = Application.objects.all()

    data = [
        {"label": "Total Companies", "count": companies.count()},
        {"label": "Total Jobs", "count": jobs.count()},
        {"label": "Total Categories", "count": categories.count()},
        {"label": "Total Applications", "count": applications.count()},
    ]

    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "data": data,
        "page_obj": page_obj,
        "sort_by": sort_by,
        "filter_by": filter_by,
        "paginator": paginator,
        "page_number": page_number,
    }

    return render(request, "job_app/dashboard.html", context)




def home(request):
    # Get top 6 categories based on the number of jobs
    categories = Category.objects.annotate(
        job_count=Count('job')).order_by('-job_count')[:8]

    # Get top 7 most recent jobs
    jobs = Job.objects.order_by('-posted_at')[:7]

    # Get all locations
    locations = Location.objects.all()
    print(locations)
    context = {
        "locations": locations,
        "categories": categories,
        "jobs": jobs
    }
    return render(request, "job_app/index.html", context)


def get_sorted_jobs(sort_by):
    sort_options = {
        'title_asc': 'title',
        'title_desc': '-title',
        'salary_asc': 'salary',
        'salary_desc': '-salary',
        'date_newest': '-posted_at',
        'date_oldest': 'posted_at',
    }
    return sort_options.get(sort_by, 'title')


def filter_jobs_by_category(job_list, category_id):
    if category_id and category_id != 'None':
        job_list = job_list.filter(job_category_id=category_id)
    return job_list


def filter_jobs_by_types(job_list, job_types):
    if job_types:
        job_list = job_list.filter(job_type__in=job_types)
    return job_list


def filter_jobs_by_location(job_list, location_id):
    if location_id and location_id != 'None':
        job_list = job_list.filter(location_id=location_id)
    return job_list


def filter_jobs_by_experience(job_list, experience_ranges):
    if experience_ranges:
        experience_filters = []
        for exp_range in experience_ranges:
            if '-' in exp_range:
                min_exp, max_exp = exp_range.split('-')
                min_exp = int(min_exp) if min_exp else 0
                max_exp = int(max_exp) if max_exp else 100
                experience_filters.append(
                    Q(min_experience_years__gte=min_exp, min_experience_years__lte=max_exp))
        job_list = job_list.filter(reduce(operator.or_, experience_filters))
    return job_list


def filter_jobs_by_posted_within(job_list, posted_within):
    if posted_within and posted_within != 'None':
        days_ago = int(posted_within)
        date_threshold = datetime.now() - timedelta(days=days_ago)
        job_list = job_list.filter(posted_at__gte=date_threshold)
    return job_list


def job_listing(request):
    sort_by = request.GET.get('sort_by', 'title_asc')
    category_id = request.GET.get('category', None)
    job_types = request.GET.getlist('job_type', [])
    location_id = request.GET.get('location', None)
    experience_ranges = request.GET.getlist('experience', [])
    posted_within = request.GET.get('posted_within', None)

    job_list = Job.objects.all()
    job_list = filter_jobs_by_category(job_list, category_id)
    job_list = filter_jobs_by_types(job_list, job_types)
    job_list = filter_jobs_by_location(job_list, location_id)
    job_list = filter_jobs_by_experience(job_list, experience_ranges)
    job_list = filter_jobs_by_posted_within(job_list, posted_within)
    job_list = job_list.order_by(get_sorted_jobs(sort_by))

    total_jobs = job_list.count()  # Get the total count of jobs

    paginator = Paginator(job_list, 30)  # Show 30 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    categories = Category.objects.all()
    locations = Location.objects.all()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,  # Pass the total count to the context
        "sort_by": sort_by,
        "categories": categories,
        "locations": locations,
        "selected_category": category_id,
        "selected_job_types": job_types,
        "selected_location": location_id,
        "selected_experience_ranges": experience_ranges,
        "selected_posted_within": posted_within,
    }
    return render(request, "job_app/job_listing.html", context)


def job_detail(request,id):
    job = get_object_or_404(Job, id=id)
    required_knowledge_list = job.required_knowledge_skills_abilities.split(
        ',')   
    education_experience_list = job.education_experience.split(
        ',')  
    context = {
        "education_experience": education_experience_list,
        "job": job, 
        "required_knowledge_list": required_knowledge_list
    }
    return render(request, "job_app/job_detail.html", context)


@staff_required
def create_or_edit_job(request, id=None):
    if id:
        job = get_object_or_404(Job, id=id)
        if request.method == "POST":
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, "Job updated successfully!")
                return redirect("job_detail", id=job.id)
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(error)
                messages.error(request, "Failed to update job. " +
                               ", ".join(error_messages))
                print(form.errors)  # Check for form errors
        else:
            form = JobForm(instance=job)
    else:
        job = None
        if request.method == "POST":
            form = JobForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Job created successfully!")
                return redirect("create_job")
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(error)
                messages.error(request, "Failed to create job. " +
                               ", ".join(error_messages))
                print(form.errors)  # Check for form errors
        else:
            form = JobForm()

    return render(request, "job_app/create_or_edit_job_form.html", {"form": form, "job": job})


@staff_required
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect("jobs")
    return redirect("job_detail", id=job.id)


@staff_required
def create_or_edit_company(request, id=None):
    if id:
        company = get_object_or_404(Company, id=id)
        if request.method == "POST":
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                return redirect("company_detail", id=company.id)
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(error)
                messages.error(
                    request, "Failed to update company. " + ", ".join(error_messages))
                print(form.errors)  # Check for form errors
        else:
            form = CompanyForm(instance=company)
    else:
        if request.method == "POST":
            form = CompanyForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Company created successfully!")
                return redirect("add_company")
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(error)
                messages.error(
                    request, "Failed to create company. " + ", ".join(error_messages))
                print(form.errors)  # Check for form errors
        else:
            form = CompanyForm()

    return render(request, "job_app/create_or_edit_company_form.html", {"form": form, "company": company if id else None})


@staff_required
def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == "POST":
        company.delete()
        return redirect("companies")
    return redirect("company_detail", id=company.id)


@staff_required
def companies(request):
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    filter_by = request.GET.get('filter', '')  # Default no filter

    companies = Company.objects.filter(
        Q(name__icontains=filter_by) |
        Q(email__icontains=filter_by) |
        Q(phone__icontains=filter_by) |
        Q(website__icontains=filter_by)
    ).order_by(sort_by)

    paginator = Paginator(companies, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "job_app/Companies.html", {"page_obj": page_obj, "sort_by": sort_by, "filter_by": filter_by})


@staff_required
def company_detail(request, id):
    company = Company.objects.get(id=id)
    return render(request, "job_app/company_detail.html", {"company": company})


@staff_required
def create_or_edit_location(request, id=None):
    if id:
        location = get_object_or_404(Location, id=id)
        if request.method == "POST":
            form = LocationForm(request.POST, instance=location)
            if form.is_valid():
                form.save()
                
                return redirect("location_detail", id=location.id)
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{error}")
                messages.error(request, "Failed to update location. " +
                               ", ".join(error_messages))
        else:
            form = LocationForm(instance=location)
    else:
        if request.method == "POST":
            form = LocationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Location Added successfully!")
                return redirect("add_location")
            else:
                error_messages = []
                for errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{error}")
                messages.error(request, "Failed to add location. " +
                               ", ".join(error_messages))
        else:
            form = LocationForm()

    return render(request, "job_app/create_or_edit_location_form.html", {"form": form, "location": location if id else None})


@staff_required
def locations(request):
    sort_by = request.GET.get('sort', 'city')  # Default sorting by city
    filter_by = request.GET.get('filter', '')  # Default no filter

    locations = Location.objects.filter(
        Q(city__icontains=filter_by) |
        Q(country__icontains=filter_by)
    ).order_by(sort_by)

    paginator = Paginator(locations, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort_by": sort_by,
        "filter_by": filter_by,
        "paginator": paginator,
        "page_number": page_number,
    }

    return render(request, "job_app/Locations.html", context)


@staff_required
def location_detail(request, id):
    location = Location.objects.get(id=id)
    return render(request, "job_app/location_detail.html", {"location":location})


@staff_required
def delete_location(request, id):
    location = get_object_or_404(Location, id=id)
    if request.method == "POST":
        location.delete()
        return redirect("locations")
    return redirect("location_detail", id=location.id)


@staff_required
def create_or_edit_category(request, id=None):
    if id:
        category = get_object_or_404(Category, id=id)
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return redirect("category_detail", id=category.id)
            else:
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                messages.error(request, "Failed to update category. " +
                               ", ".join(error_messages))
        else:
            form = CategoryForm(instance=category)
    else:
        if request.method == "POST":
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect("add_category")
            else:
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                messages.error(request, "Failed to add category. " +
                               ", ".join(error_messages))
        else:
            form = CategoryForm()

    return render(request, "job_app/create_or_edit_category_form.html", {"form": form, "category": category if id else None})


@staff_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect("categoreis")
    return redirect("category_detail", id=category.id)


@staff_required
def categories(request):
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    filter_by = request.GET.get('filter', '')  # Default no filter

    categories = Category.objects.filter(
        Q(name__icontains=filter_by)
    ).order_by(sort_by)

    paginator = Paginator(categories, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "job_app/Category.html", {"page_obj": page_obj, "sort_by": sort_by, "filter_by": filter_by})


@staff_required
def category_detail(request, id):
    category = Category.objects.get(id=id)
    return render(request, "job_app/category_detail.html", {"category": category})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your message has been sent successfully!")
            return redirect("contact")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, "Failed to send your message. " +
                           ", ".join(error_messages))
    else:
        form = ContactForm()
    return render(request, "job_app/contact.html", {"form": form})
        

def contact_view(request):
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    filter_by = request.GET.get('filter', '')  # Default no filter

    contacts = Contact.objects.filter(
        Q(name__icontains=filter_by) |
        Q(email__icontains=filter_by) |
        Q(subject__icontains=filter_by)
    ).order_by(sort_by)

    paginator = Paginator(contacts, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort_by": sort_by,
        "filter_by": filter_by,
        "paginator": paginator,
        "page_number": page_number,
    }

    return render(request, "job_app/contact_table.html", context)


def contact_detail(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, "job_app/contact_detail.html", {"contact": contact})


def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            messages.success(
                request, "Your Application has been sent successfully!")
            return redirect("jobs")
    else:
        form = ApplicationForm(initial={'job': job.id})
    return render(request, 'job_app/apply_form.html', {'form': form, 'job': job})


def application_list_view(request):
    # Default sorting by full_name
    sort_by = request.GET.get('sort', 'full_name')
    filter_by = request.GET.get('filter', '')  # Default no filter

    applications = Application.objects.filter(
        Q(full_name__icontains=filter_by) |
        Q(city__icontains=filter_by) |
        Q(job__title__icontains=filter_by) |
        Q(job__company__name__icontains=filter_by)
    ).order_by(sort_by)

    paginator = Paginator(applications, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort_by": sort_by,
        "filter_by": filter_by,
        "paginator": paginator,
        "page_number": page_number,
    }
    return render(request, 'job_app/application.html', context)


def application_detail(request, id):
    application = Application.objects.get(id=id)
    return render(request, "job_app/application_detail.html", {"application": application})





