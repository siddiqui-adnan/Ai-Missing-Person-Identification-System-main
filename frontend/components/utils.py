"""
Utility functions for UI components
"""
import streamlit as st
import base64
from datetime import datetime


def format_time_12h(dt):
    """Format datetime to 12-hour format with AM/PM"""
    if dt is None:
        return "Unknown"
    return dt.strftime('%Y-%m-%d %I:%M %p')


def get_indian_states_and_cities():
    """Return Indian states and their cities for dropdowns"""
    indian_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
        "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]
    
    state_cities = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Tirupati", "Kadapa", "Kakinada", "Anantapur", "Vizianagaram", "Eluru", "Ongole", "Nandyal", "Machilipatnam", "Adoni", "Tenali", "Chittoor", "Hindupur", "Proddatur", "Bhimavaram", "Madanapalle", "Guntakal", "Dharmavaram", "Gudivada", "Srikakulam", "Narasaraopet", "Rajampet", "Tadpatri", "Tadepalligudem"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro", "Bomdila", "Tezu", "Seppa", "Changlang", "Aalo"],
        "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon", "Karimganj", "Dhubri", "Diphu", "North Lakhimpur", "Goalpara", "Barpeta", "Sivasagar", "Golaghat", "Haflong", "Mangaldoi", "Lumding", "Hailakandi"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif", "Arrah", "Begusarai", "Katihar", "Munger", "Chhapra", "Danapur", "Saharsa", "Sasaram", "Hajipur", "Dehri", "Siwan", "Motihari", "Nawada", "Bagaha", "Buxar", "Kishanganj", "Sitamarhi", "Jamalpur", "Jehanabad", "Aurangabad"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon", "Jagdalpur", "Raigarh", "Ambikapur", "Mahasamund", "Dhamtari", "Chirmiri", "Bhatapara", "Dalli-Rajhara", "Naila Janjgir", "Tilda Newra", "Mungeli", "Manendragarh", "Sakti"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Bicholim", "Curchorem", "Sanquelim", "Cuncolim", "Quepem", "Canacona", "Pernem"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar", "Gandhidham", "Anand", "Navsari", "Morbi", "Nadiad", "Surendranagar", "Bharuch", "Mehsana", "Bhuj", "Porbandar", "Palanpur", "Valsad", "Vapi", "Gondal", "Veraval", "Godhra", "Patan", "Kalol", "Dahod", "Botad", "Amreli", "Deesa"],
        "Haryana": ["Faridabad", "Gurugram", "Hisar", "Rohtak", "Panipat", "Karnal", "Sonipat", "Yamunanagar", "Panchkula", "Bhiwani", "Bahadurgarh", "Jind", "Sirsa", "Thanesar", "Kaithal", "Palwal", "Rewari", "Hansi", "Narnaul", "Fatehabad", "Gohana", "Tohana"],
        "Himachal Pradesh": ["Shimla", "Mandi", "Solan", "Nahan", "Sundarnagar", "Palampur", "Kullu", "Hamirpur", "Una", "Dharamshala", "Bilaspur", "Chamba", "Kangra", "Manali", "Baddi", "Nalagarh", "Parwanoo", "Dalhousie"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro Steel City", "Deoghar", "Phusro", "Hazaribagh", "Giridih", "Ramgarh", "Medininagar", "Chirkunda", "Dumka", "Sahibganj", "Chaibasa", "Gumla", "Godda"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi", "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga", "Tumakuru", "Raichur", "Bidar", "Hosapete", "Hassan", "Gadag", "Udupi", "Robertson Pet", "Bhadravati", "Chitradurga", "Kolar", "Mandya", "Chikkamagaluru", "Gangavati", "Bagalkote", "Ranebennuru"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Palakkad", "Alappuzha", "Malappuram", "Kannur", "Kottayam", "Kasaragod", "Pathanamthitta", "Idukki", "Wayanad", "Ernakulam", "Thalassery", "Ponnani", "Vatakara", "Kanhangad", "Payyanur", "Koyilandy", "Parappanangadi", "Kalamassery", "Neyyattinkara", "Tanur", "Kayamkulam", "Thrippunithura", "Muvattupuzha", "Pala", "Cherthala"],
        "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam", "Rewa", "Katni", "Singrauli", "Burhanpur", "Khandwa", "Morena", "Bhind", "Chhindwara", "Guna", "Shivpuri", "Vidisha", "Chhatarpur", "Damoh", "Mandsaur", "Khargone", "Neemuch", "Pithampur", "Hoshangabad", "Itarsi", "Sehore", "Betul"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Kalyan-Dombivli", "Vasai-Virar", "Chhatrapati Sambhajinagar", "Navi Mumbai", "Solapur", "Mira-Bhayandar", "Bhiwandi", "Amravati", "Nanded", "Kolhapur", "Ulhasnagar", "Sangli-Miraj-Kupwad", "Malegaon", "Jalgaon", "Akola", "Latur", "Dhule", "Ahmednagar", "Ichalkaranji", "Parbhani", "Panvel", "Yavatmal", "Achalpur", "Osmanabad", "Nandurbar", "Satara", "Wardha", "Udgir", "Beed"],
        "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Kakching", "Ukhrul", "Senapati", "Tamenglong", "Jiribam"],
        "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongpoh", "Baghmara", "Cherrapunji", "Mairang", "Resubelpara"],
        "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai", "Kolasib", "Serchhip", "Lawngtlai", "Mamit"],
        "Nagaland": ["Dimapur", "Kohima", "Mokokchung", "Tuensang", "Zunheboto", "Wokha", "Mon", "Phek", "Kiphire", "Longleng", "Peren"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Baripada", "Jharsuguda", "Brahmapur", "Rourkela", "Angul", "Bhadrak", "Jajpur", "Kendrapara", "Kendujhar", "Keonjhar", "Koraput", "Mayurbhanj", "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundargarh"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Firozpur", "Pathankot", "Batala", "Moga", "Abohar", "Jalandhar", "Kapurthala", "Hoshiarpur", "Nawanshahr", "Rupnagar", "Sangrur", "Fazilka", "Faridkot", "Gurdaspur", "Mansa", "Barnala", "Tarn Taran"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer", "Bhilwara", "Alwar", "Sikar", "Bharatpur", "Pali", "Sri Ganganagar", "Churu", "Tonk", "Baran", "Dholpur", "Hanumangarh", "Jhunjhunu", "Karauli", "Nagaur", "Pratapgarh", "Rajsamand", "Sawai Madhopur", "Sirohi", "Dausa", "Dungarpur", "Jaisalmer", "Jhalawar", "Sikar"],
        "Sikkim": ["Gangtok", "Namchi", "Geyzing", "Mangan", "Pelling", "Jorethang", "Rangpo", "Singtam", "Ravangla"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Erode", "Tirunelveli", "Vellore", "Thoothukudi", "Dindigul", "Thanjavur", "Ranipet", "Nagercoil", "Sivakasi", "Karur", "Kanchipuram", "Kumbakonam", "Cuddalore", "Tiruppur", "Dharmapuri", "Ariyalur", "Krishnagiri", "Nagapattinam", "Namakkal", "Perambalur", "Pudukkottai", "Ramanathapuram", "Sivaganga", "Tiruvallur", "Tiruvarur", "Viluppuram", "Virudhunagar"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar", "Ramagundam", "Mahbubnagar", "Nalgonda", "Miryalaguda", "Adilabad", "Nirmal", "Suryapet", "Jagtial", "Peddapalli", "Kothagudem", "Bhadrachalam", "Mancherial", "Bellampalli", "Mandamarri", "Chennur", "Sangareddy", "Medak", "Siddipet", "Jangaon", "Yellandu", "Palwancha", "Kothagudem"],
        "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Kailashahar", "Belonia", "Khowai", "Ranirbazar", "Sonamura", "Melaghar", "Amirpur"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut", "Allahabad", "Ghaziabad", "Noida", "Bareilly", "Aligarh", "Moradabad", "Saharanpur", "Gorakhpur", "Firozabad", "Jhansi", "Mathura", "Rampur", "Bulandshahr", "Muzaffarnagar", "Shahjahanpur", "Sitapur", "Etawah", "Faizabad", "Bijnor", "Mirzapur", "Sultanpur", "Deoria", "Bahraich", "Unnao", "Azamgarh", "Orai", "Lakhimpur", "Budaun", "Hapur", "Shikohabad", "Shamli", "Mau", "Chandausi", "Khurja", "Sambhal", "Nagina", "Tilhar", "Nawabganj", "Nanpara", "Bisalpur", "Pilibhit", "Shahganj", "Tanda", "Amroha", "Amethi", "Rae Bareli", "Barabanki", "Lalitpur", "Jalaun", "Hamirpur", "Mahoba", "Banda", "Chitrakoot", "Fatehpur", "Kaushambi", "Pratapgarh", "Sant Kabir Nagar", "Siddharthnagar", "Basti", "Gonda", "Balrampur", "Shrawasti", "Bahraich"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Kashipur", "Rishikesh", "Pithoragarh", "Ramnagar", "Jaspur", "Tehri", "Pauri", "Nainital", "Almora", "Champawat", "Bageshwar", "Rudraprayag", "Uttarkashi"],
        "West Bengal": ["Kolkata", "Asansol", "Siliguri", "Durgapur", "Bardhaman", "Malda", "Baharampur", "Habra", "Kharagpur", "Shantipur", "Dankuni", "Dhulian", "Ranaghat", "Haldia", "Raiganj", "Krishnanagar", "Nabadwip", "Medinipur", "Jalpaiguri", "Balurghat", "Basirhat", "Bankura", "Chakdaha", "Darjeeling", "Alipurduar", "Purulia", "Jangipur", "Bangaon", "Cooch Behar"],
        "Andaman and Nicobar Islands": ["Port Blair", "Diglipur", "Rangat", "Mayabunder", "Car Nicobar", "Nancowry", "Campbell Bay"],
        "Chandigarh": ["Chandigarh"],
        "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
        "Delhi": ["New Delhi", "Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi", "North East Delhi", "North West Delhi", "South East Delhi", "South West Delhi", "Shahdara", "Dwarka", "Rohini", "Najafgarh"],
        "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Sopore", "Kathua", "Udhampur", "Poonch", "Rajouri"],
        "Ladakh": ["Leh", "Kargil", "Nubra", "Zanskar"],
        "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Andrott", "Minicoy"],
        "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"]
    }
    
    return indian_states, state_cities


@st.cache_data
def load_background_image():
    """Load and encode background image"""
    try:
        with open("assets/background.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""


@st.cache_data
def load_config():
    """Load authentication configuration"""
    import yaml
    from yaml import SafeLoader
    
    try:
        with open("login_config.yml") as file:
            return yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        st.error("Configuration file 'login_config.yml' not found")
        st.stop()
        return None
