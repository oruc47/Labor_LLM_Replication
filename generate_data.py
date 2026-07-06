

import json
import os
import random


random.seed(0)

DATA_DIR = "data"

N_WORKERS = 5000

sectors = {
    "food_service": [
        "Cashiers",
        "Waiters and waitresses",
        "Cooks",
        "Maids and housekeeping cleaners",
        "Food preparation workers",
        "Dishwashers",
        "Bartenders",
        "Fast food workers",
        "Short order cooks",
        "Bakers",
        "Kitchen managers",
        "Food service managers",
        "Busers and dining room attendants",
        "Pastry chefs",
        "Head cooks",
        "Sous chefs",
        "Line cooks",
    ],
    "office_admin": [
        "Secretaries and administrative assistants",
        "Bookkeeping, accounting, and auditing clerks",
        "Receptionists and information clerks",
        "Data entry keyers",
        "Office clerks, general",
        "Payroll specialists",
        "Human resources specialists",
        "Executive secretaries and administrative assistants",
        "Medical secretaries",
        "Legal secretaries",
        "Billing and posting clerks",
        "Customer service representatives",
        "Scheduling coordinators",
        "Records clerks",
        "Compliance officers",
    ],
    "sales": [
        "Retail salespersons",
        "First-line supervisors/managers of retail sales workers",
        "Sales Representatives Services All Other",
        "Sales managers",
        "Real estate brokers",
        "Real estate sales agents",
        "Insurance sales agents",
        "Securities and commodities sales agents",
        "Wholesale and manufacturing sales representatives",
        "Advertising sales agents",
        "Travel agents",
        "Door-to-door sales workers",
        "Parts salespersons",
        "Cashiers in retail",
        "Stock clerks and order fillers",
    ],
    "health": [
        "Nursing, psychiatric, and home health aides",
        "Licensed practical and licensed vocational nurses",
        "Registered nurses",
        "Physicians and surgeons",
        "Dentists",
        "Physician assistants",
        "Nurse practitioners",
        "Clinical nurses",
        "Surgical nurses",
        "Pediatric nurses",
        "Psychiatric nurses",
        "Emergency medical technicians and paramedics",
        "Medical and health services managers",
        "Medical assistants",
        "Dental hygienists",
        "Dental assistants",
        "Phlebotomists",
        "Medical laboratory technicians",
        "Radiology technologists",
        "Physical therapy assistants",
        "Occupational therapy assistants",
    ],
    "trades": [
        "Painting workers",
        "Construction laborers",
        "Carpenters",
        "Automotive service technicians and mechanics",
        "Electricians",
        "Plumbers and pipefitters",
        "Heating and air conditioning mechanics and installers",
        "Diesel engine specialists",
        "Welders, cutters, solderers, and brazers",
        "Heavy equipment operators",
        "Equipment operators, all other",
        "Roofers",
        "Brickmasons, blockmasons, and stonemasons",
        "Tile and marble setters",
        "Concrete workers",
        "Insulation workers",
        "Glaziers",
        "Ironworkers",
        "Machine operators, general",
        "Tool and die makers",
    ],
    "professional": [
        "Accountants and auditors",
        "Elementary and middle school teachers",
        "Computer programmers",
        "Software developers",
        "Computer systems analysts",
        "Information security analysts",
        "Database administrators",
        "Network administrators",
        "Web developers",
        "Data scientists",
        "High school teachers",
        "College and university teachers",
        "Lawyers",
        "Judges and magistrates",
        "Paralegals and legal assistants",
        "Engineers, all types",
        "Architects",
        "Urban and regional planners",
        "Graphic designers",
        "Interior designers",
        "Surveyors and cartographers",
        "Mathematicians and statisticians",
    ],
    "transportation_logistics": [
        "Heavy and tractor-trailer truck drivers",
        "Light truck or delivery services drivers",
        "Bus drivers, transit and intercity",
        "Taxi drivers and chauffeurs",
        "Parking lot attendants",
        "Motorcycle taxi drivers",
        "Warehouse and stockroom workers",
        "Shipping and receiving clerks",
        "Logistics coordinators",
        "Delivery drivers",
        "Dispatch supervisors",
        "Freight and cargo inspectors",
        "Dock workers and longshoremen",
        "Material movers, manual",
        "Forklift operators",
    ],
    "manufacturing": [
        "Assembly and fabricators",
        "Production workers, all other",
        "Quality control inspectors",
        "Packaging and filling machine operators",
        "Laundry and dry-cleaning workers",
        "Textile machine operators",
        "Printing machine operators",
        "Upholsterers",
        "Jewelers and precious stone and metal workers",
        "Woodworkers",
        "Inspectors, testers, sorters, samplers, and weighers",
        "Plant operators",
        "Chemical technicians",
        "Petroleum technicians",
    ],
    "maintenance_repair": [
        "General maintenance and repair workers",
        "Building maintenance workers",
        "Maintenance workers, machinery",
        "Millwrights",
        "Locksmiths and safe repairers",
        "Coin, vending, and amusement machine servicers and repairers",
        "Appliance repairers",
        "Refractory materials repairers, except brickmasons",
        "Helpers, installation, maintenance, and repair workers",
        "Aircraft mechanics and service technicians",
        "Small engine mechanics",
        "Bicycle repairers",
    ],
    "protective_services": [
        "Police and sheriff's patrol officers",
        "Detectives and criminal investigators",
        "Fire fighters",
        "Fire inspectors",
        "Security guards",
        "Gaming surveillance officers",
        "Correctional officers",
        "Bailiffs",
        "Loss prevention specialists",
        "Crossing guards",
        "First-line supervisors of police and detectives",
        "Lifeguards",
    ],
    "education": [
        "Elementary school teachers",
        "Middle school teachers",
        "High school teachers",
        "Special education teachers",
        "Adult basic education and literacy teachers",
        "Postsecondary education teachers",
        "Teacher assistants",
        "Education administrators",
        "Librarians",
        "Library technicians",
        "School counselors",
        "Educational psychologists",
        "Instructional coordinators",
    ],
    "social_services": [
        "Social and human service assistants",
        "Mental health and substance abuse social workers",
        "Child, family, and school social workers",
        "Healthcare social workers",
        "Community and social service managers",
        "Counselors, all other",
        "Marriage and family therapists",
        "Rehabilitation counselors",
        "Probation officers and correctional treatment specialists",
        "Case workers",
        "Social and community service managers",
    ],
    "hospitality_leisure": [
        "Hotel, motel, and resort desk clerks",
        "Hotel managers",
        "Casino workers",
        "Amusement and recreation attendants",
        "Fitness trainers and aerobics instructors",
        "Coaches and scouts",
        "Recreational therapists",
        "Recreation workers",
        "Ushers, lobby attendants, and ticket takers",
        "Museum technicians and conservators",
    ],
    "media_entertainment": [
        "Actors",
        "Producers and directors",
        "Radio and television announcers",
        "Journalists and news analysts",
        "Photographers",
        "Camera operators",
        "Video editors",
        "Sound engineering technicians",
        "Musicians and singers",
        "Dancers and choreographers",
        "Film and video editors",
        "Makeup artists",
        "Art directors",
    ],
    "agricultural_natural_resources": [
        "Farmers and ranchers",
        "Farm labor contractors",
        "Agricultural workers, all other",
        "Fishing and hunting workers",
        "Forest and conservation technicians",
        "Forest and conservation workers",
        "Logging equipment operators",
        "Forestry aides",
        "Soil scientists",
        "Botanists",
    ],
    "personal_care_services": [
        "Personal care and service supervisors",
        "Hairdressers, hairstylists, and cosmetologists",
        "Barbers",
        "Estheticians and skin care specialists",
        "Shampooers",
        "Nail technicians",
        "Massage therapists",
        "Spa attendants",
        "Fitness attendants",
        "Nannies and babysitters",
        "Childcare workers",
        "Personal attendants",
        "Companions and home health aides",
    ],
    "finance_insurance": [
        "Financial managers",
        "Personal financial advisors",
        "Financial analysts",
        "Budget analysts",
        "Credit analysts",
        "Loan officers",
        "Insurance underwriters",
        "Insurance claims and policy processing clerks",
        "Insurance adjusters, examiners, and investigators",
        "Actuaries",
        "Bank tellers",
        "Brokerage clerks",
        "Investment fund managers",
    ],
    "marketing_communications": [
        "Marketing managers",
        "Advertising managers",
        "Public relations managers",
        "Market research analysts",
        "Advertising specialists",
        "Marketing coordinators",
        "Social media specialists",
        "Content strategists",
        "Public relations specialists",
        "Copywriters",
        "Brand managers",
        "Digital marketing analysts",
    ],
    "business_operations": [
        "General and operations managers",
        "Management analysts",
        "Business operations specialists",
        "Project managers",
        "Program coordinators",
        "Administrative services managers",
        "Facilities managers",
        "Property managers",
        "Asset managers",
        "Supply chain managers",
        "Procurement specialists",
        "Quality assurance managers",
    ],
    "scientific_technical": [
        "Biological scientists",
        "Microbiologists",
        "Environmental scientists and specialists",
        "Geoscientists",
        "Physicists and astronomers",
        "Chemists",
        "Chemical technicians",
        "Geological and petroleum technicians",
        "Laboratory technicians",
        "Survey technicians",
    ],
}


special_states = ["In education", "Unemployed", "Not in labor force"]



all_jobs = []

for jobs in sectors.values():
    for job in jobs:
        all_jobs.append(job)

all_jobs.extend(special_states)


job_sector = {}

for sector, jobs in sectors.items():
    for job in jobs:
        job_sector[job] = sector


entry_jobs = ["In education", "Cashiers", "Waiters and waitresses",
              "Retail salespersons", "Nursing, psychiatric, and home health aides",
              "Construction laborers"]


#distribution of demographics taken directly from LaborLLM paper

gender_dist    = {"male": 0.50, "female": 0.50}
region_dist    = {"south": 0.40, "northcentral": 0.24, "west": 0.19, "northeast": 0.17}
ethnicity_dist = {"white": 0.55, "black or african american": 0.28, "hispanic": 0.17}


def sample_from(distribution):
    return random.choices(list(distribution.keys()), weights = list(distribution.values()))[0]


STAY = 0.55
SAME_SECTOR = 0.28
TO_NONEMPLOYMENT = 0.14
OTHER_SECTOR = 0.03



#If someone is in a job, what are their transition probabilities
def job_transitions(job):
    weights = {job: STAY}

    mates = []

    for j in sectors[job_sector[job]]:
        if j != job:
            mates.append(j)

    for j in mates:
        weights[j] = SAME_SECTOR / len(mates)

    weights["Unemployed"] = TO_NONEMPLOYMENT * 0.6
    weights["Not in labor force"] = TO_NONEMPLOYMENT * 0.4

    others = []

    for s, jobs in sectors.items():
        if s != job_sector[job]:
            for j in jobs:
                others.append(j)

    for j in others:
        weights[j] = OTHER_SECTOR / len(others)
    return weights

#If someone is in a non-employment state, what do they do next year?
def special_state_transitions(state):

    employed = []

    for j in all_jobs:
        if j not in special_states:
            employed.append(j)

    if state == "In education":
        w = {"In education": 0.45}
        starters = [j for j in entry_jobs if j != "In education"]
        for j in starters:
            w[j] = 0.55 / len(starters)
    elif state == "Unemployed":
        w = {"Unemployed": 0.35, "Not in labor force": 0.10}
        for j in employed:
            w[j] = 0.55 / len(employed)
    else:  # "Not in labor force"
        w = {"Not in labor force": 0.70, "Unemployed": 0.10}
        for j in employed:
            w[j] = 0.20 / len(employed)
    return w


transitions = {}

for job in all_jobs:
    transitions[job] = (special_state_transitions(job) if job in special_states else job_transitions(job))


def sample_next(current_job):
    options = transitions[current_job]
    return random.choices(list(options.keys()), weights=list(options.values()))[0]

def generate_worker():
    birth_year = random.randint(1955, 1995)
    start_year = birth_year + random.randint(18,22)
    n_years = int(random.triangular(4, 25, 12))

    job = random.choice(entry_jobs)
    career = []
    for i in range(n_years):
        career.append((start_year + i, job))
        job = sample_next(job)

    return {
            "gender" : sample_from(gender_dist),
            "ethnicity" : sample_from(ethnicity_dist),
            "region" : sample_from(region_dist),
            "birth_year" : birth_year,
            "career" : career,
            }

def make_resume(worker):
    lines = ["<A synthetic worker>"]
    lines.append(
            f"The following information is available about the work history of a {worker["gender"]} {worker["ethnicity"]} worker residing in the {worker["region"]} region."
            )

    lines.append(f"The worker was born in {worker["birth_year"]}.")

    lines.append("The worker has the following records of work experience, one entry per line, including year and the job title:")

    for year, job in worker["career"]:
        lines.append(f"{year} : {job}")
    lines.append("<END OF DATA>")
    return "\n".join(lines)

workers = []

for _ in range(N_WORKERS):
    workers.append(generate_worker())


n_train = int(0.70 * N_WORKERS)
n_val = int(0.1 * N_WORKERS)
train = workers[:n_train]
val = workers[n_train:n_train + n_val]
test = workers[n_train + n_val:]


def save_jsonl(filename, group):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        for w in group:
            f.write(json.dumps({"worker" : w, "text" : make_resume(w)}) + "\n")


save_jsonl("train.jsonl", train)
save_jsonl("val.jsonl", val)
save_jsonl("test.jsonl", test)

with open(os.path.join(DATA_DIR, "meta.json"), "w") as f:
    json.dump({"all_jobs": all_jobs, "sectors": sectors, "special_states": special_states, "transitions" : transitions}, f, indent=2)




print("=== Synthetic dataset summary ===")
print(f"workers            : {N_WORKERS}  (train {len(train)}, val {len(val)}, test {len(test)})")

