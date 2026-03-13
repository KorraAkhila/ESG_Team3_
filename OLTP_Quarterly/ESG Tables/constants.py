# constants.py

SYSTEM_USER = "system"

# Master Lists for Random Selection

DATA_SOURCES = ["Meter Reading", "Invoice", "ERP Export"]

DOCUMENT_TYPES_MASTER = [
    (1, "Fuel Invoice"),
    (2, "Meter Reading"),
    (3, "Fuel Purchase Receipt"),
    (4, "Supplier Statement"),
    (5, "Log Book"),
    (6, "Weighbridge Slip"),
    (7, "Energy Bill"),
    (8, "Transport Fuel Bill")
]

LOCATIONS = [
    "Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Hyderabad, Telangana",
    "Pune, Maharashtra", "Mumbai, Maharashtra", "Ahmedabad, Gujarat",
    "Coimbatore, Tamil Nadu", "Nagpur, Maharashtra", "Noida, Uttar Pradesh",
    "Kolkata, West Bengal"
]

# ORGANIZATIONS = [
#     (1, "Tata Consultancy Services Ltd", "IT services and consulting company with global operations", "2022-03-15 10:45:30"),
#     (2, "Infosys Limited", "Digital services and consulting organization focusing on sustainability", "2021-11-08 09:20:10"),
#     (3, "Reliance Industries Limited", "Diversified conglomerate with energy, petrochemicals, and retail businesses", "2020-07-22 14:10:55"),
#     (4, "Larsen & Toubro Ltd", "Engineering, construction, and heavy manufacturing enterprise", "2021-02-18 16:35:40"),
#     (5, "Mahindra & Mahindra Ltd", "Automotive and farm equipment manufacturing company", "2022-08-01 11:05:00"),
#     (6, "Adani Ports and SEZ Ltd", "Port infrastructure and logistics services provider", "2023-01-12 13:50:25"),
#     (7, "Hindustan Unilever Ltd", "FMCG manufacturer with large production facilities", "2021-06-30 08:40:15"),
#     (8, "JSW Steel Ltd", "Integrated steel manufacturing company", "2020-09-19 17:25:45"),
#     (9, "Bharat Petroleum Corporation Ltd", "Oil refining and fuel distribution company", "2022-12-05 10:15:20"),
#     (10, "ITC Limited", "FMCG, hotels, paperboards, and agribusiness company", "2021-04-10 15:00:00"),
#     (11, "NTPC Limited", "Thermal and renewable power generation company", "2020-05-22 09:30:00"),
#     (12, "Coal India Limited", "Coal mining and production company", "2019-11-14 14:55:00"),
#     (13, "Oil and Natural Gas Corporation Ltd", "Oil and gas exploration and production company", "2020-01-08 11:10:10"),
#     (14, "Indian Oil Corporation Ltd", "Petroleum refining and fuel retailing company", "2021-09-02 16:00:00"),
#     (15, "Power Grid Corporation of India Ltd", "Power transmission and infrastructure company", "2022-02-11 12:45:20"),
#     (16, "UltraTech Cement Ltd", "Cement manufacturing company", "2020-10-18 09:20:45"),
#     (17, "Grasim Industries Ltd", "Cement, textiles, and chemicals manufacturing company", "2021-07-14 15:35:10"),
#     (18, "Shree Cement Ltd", "Cement production and distribution company", "2022-06-05 10:50:30"),
#     (19, "Tata Steel Ltd", "Steel manufacturing and processing company", "2019-12-20 14:15:55"),
#     (20, "Vedanta Limited", "Mining and natural resources company", "2020-03-09 11:05:40"),
#     (21, "Maruti Suzuki India Ltd", "Passenger vehicle manufacturing company", "2021-01-25 09:45:00"),
#     (22, "Hero MotoCorp Ltd", "Two-wheeler manufacturing company", "2022-04-18 13:20:10"),
#     (23, "Bajaj Auto Ltd", "Automotive manufacturing company", "2020-08-07 10:00:00"),
#     (24, "Ashok Leyland Ltd", "Commercial vehicle manufacturing company", "2021-10-29 15:40:00"),
#     (25, "Tata Motors Ltd", "Automobile manufacturing company", "2020-06-13 12:30:45"),
#     (26, "Dr. Reddy’s Laboratories Ltd", "Pharmaceutical manufacturing company", "2021-05-06 11:10:30"),
#     (27, "Sun Pharmaceutical Industries Ltd", "Pharmaceutical manufacturing and research company", "2022-09-22 16:20:00"),
#     (28, "Cipla Limited", "Pharmaceutical manufacturing company", "2020-04-15 09:00:00"),
#     (29, "Aurobindo Pharma Ltd", "Bulk drug and formulation manufacturing company", "2021-08-12 14:45:00"),
#     (30, "Lupin Limited", "Pharmaceutical research and manufacturing company", "2022-11-03 10:25:40"),
#     (31, "Asian Paints Ltd", "Paint and coatings manufacturing company", "2020-02-19 11:55:20"),
#     (32, "Berger Paints India Ltd", "Decorative and industrial paints manufacturer", "2021-06-21 09:35:00"),
#     (33, "ACC Limited", "Cement and building materials manufacturing company", "2020-09-28 13:15:45"),
#     (34, "Ambuja Cements Ltd", "Cement manufacturing and distribution company", "2021-12-02 10:10:00"),
#     (35, "Hindalco Industries Ltd", "Aluminium and copper manufacturing company", "2020-11-11 14:20:30"),
#     (36, "JSW Energy Ltd", "Thermal and renewable power generation company", "2022-01-05 15:30:00"),
#     (37, "Tata Power Company Ltd", "Power generation and distribution company", "2021-03-18 12:05:15"),
#     (38, "Torrent Power Ltd", "Power generation and distribution company", "2020-07-07 09:50:00"),
#     (39, "Godrej & Boyce Mfg. Co. Ltd", "Industrial manufacturing and consumer products company", "2022-05-27 11:40:10"),
#     (40, "Bosch Limited", "Automotive components manufacturing company", "2021-09-16 14:55:25"),
#     (41, "Siemens India Ltd", "Industrial automation and manufacturing company", "2020-10-05 10:30:00"),
#     (42, "ABB India Ltd", "Power and automation technology company", "2021-04-23 13:45:00"),
#     (43, "Schneider Electric India Pvt Ltd", "Energy management and automation solutions provider", "2022-02-14 09:20:00"),
#     (44, "Blue Star Limited", "HVAC and cooling systems manufacturing company", "2020-12-19 15:15:30"),
#     (45, "Voltas Limited", "Air conditioning and engineering solutions company", "2021-07-03 11:00:00"),
#     (46, "Tata Chemicals Ltd", "Chemicals and specialty products manufacturing company", "2020-05-10 14:10:00"),
#     (47, "Gujarat Alkalies and Chemicals Ltd", "Chemicals manufacturing company", "2022-03-29 10:40:00"),
#     (48, "NMDC Limited", "Iron ore mining company", "2019-08-24 09:35:00"),
#     (49, "Steel Authority of India Ltd", "Integrated steel manufacturing company", "2020-01-30 16:00:00"),
#     (50, "GAIL (India) Limited", "Natural gas processing and distribution company", "2021-11-19 12:25:00"),
#     (51, "Flipkart Internet Pvt Ltd", "E-commerce marketplace and logistics platform", "2020-07-01 10:00:00"),
#     (52, "Amazon India Pvt Ltd", "E-commerce and cloud services provider", "2019-06-15 09:30:00"),
#     (53, "Mphasis Ltd", "IT solutions and cloud services company", "2021-08-20 11:15:00"),
#     (54, "Persistent Systems Ltd", "Digital engineering and software services company", "2022-02-10 14:10:00"),
#     (55, "Coforge Ltd", "Global IT and digital services company", "2021-11-05 12:40:00"),
#     (56, "Tata Communications Ltd", "Global digital infrastructure and connectivity provider", "2020-09-18 15:20:00"),
#     (57, "IRCTC Ltd", "Railway ticketing, catering, and tourism services", "2019-10-14 09:00:00"),
#     (58, "Container Corporation of India Ltd", "Rail-based logistics and container transport company", "2020-03-22 10:35:00"),
#     (59, "Delhivery Ltd", "Integrated logistics and supply chain services company", "2022-05-01 11:50:00"),
#     (60, "Blue Dart Express Ltd", "Courier and integrated express logistics company", "2019-08-12 14:25:00"),

#     (61, "L&T Construction", "Infrastructure construction and project execution company", "2020-01-10 09:45:00"),
#     (62, "IRB Infrastructure Developers Ltd", "Road and highway infrastructure development company", "2019-07-19 13:10:00"),
#     (63, "GMR Infrastructure Ltd", "Airport and energy infrastructure company", "2021-04-02 11:30:00"),
#     (64, "GVK Industries Ltd", "Energy and infrastructure development company", "2020-12-15 10:20:00"),
#     (65, "KEC International Ltd", "Power transmission and infrastructure engineering company", "2022-06-18 14:55:00"),

#     (66, "JSPL (Jindal Steel & Power Ltd)", "Steel manufacturing and power generation company", "2021-03-12 10:05:00"),
#     (67, "Rashtriya Ispat Nigam Ltd", "Integrated steel manufacturing company (Vizag Steel)", "2019-09-05 11:40:00"),
#     (68, "Electrosteel Castings Ltd", "Ductile iron pipes and fittings manufacturer", "2020-11-28 15:00:00"),

#     (69, "Canara Bank", "Public sector banking and financial services company", "2018-06-30 09:00:00"),
#     (70, "Punjab National Bank", "Public sector bank providing retail and corporate banking", "2019-05-10 10:30:00"),
#     (71, "Union Bank of India", "Government-owned commercial bank", "2020-02-18 11:10:00"),
#     (72, "Bank of Baroda", "Public sector banking and financial services provider", "2019-03-25 09:50:00"),

#     (73, "LIC Housing Finance Ltd", "Housing finance and mortgage lending company", "2021-01-08 14:20:00"),
#     (74, "Shriram Finance Ltd", "Retail and commercial vehicle financing company", "2022-07-22 12:35:00"),
#     (75, "Cholamandalam Investment & Finance", "Vehicle and SME finance company", "2020-04-17 10:40:00"),

#     (76, "Tata Consumer Products Ltd", "Food and beverage consumer products company", "2020-10-09 11:25:00"),
#     (77, "Godrej Industries Ltd", "Diversified chemicals and consumer products company", "2019-12-20 13:45:00"),
#     (78, "Emami Ltd", "Consumer goods and personal care company", "2021-06-14 09:30:00"),
#     (79, "ITC Hotels Ltd", "Hospitality and luxury hotel chain", "2022-03-05 15:15:00"),

#     (80, "JK Cement Ltd", "Cement manufacturing company", "2020-08-30 10:10:00"),
#     (81, "Orient Cement Ltd", "Cement manufacturing and distribution company", "2021-02-19 11:50:00"),
#     (82, "HeidelbergCement India Ltd", "Cement and building materials manufacturer", "2019-11-01 09:40:00"),

#     (83, "Torrent Pharmaceuticals Ltd", "Pharmaceutical research and manufacturing company", "2020-05-28 14:05:00"),
#     (84, "Alkem Laboratories Ltd", "Generic pharmaceutical manufacturing company", "2021-09-17 10:55:00"),
#     (85, "Glenmark Pharmaceuticals Ltd", "Research-led global pharmaceutical company", "2022-01-12 13:30:00"),

#     (86, "Max Healthcare Institute Ltd", "Hospital and healthcare services provider", "2020-06-06 09:20:00"),
#     (87, "Fortis Healthcare Ltd", "Integrated healthcare delivery services company", "2019-08-15 10:45:00"),

#     (88, "Tata Elxsi Ltd", "Design and technology services company", "2021-12-09 11:10:00"),
#     (89, "KPIT Technologies Ltd", "Automotive software and embedded systems company", "2022-04-21 14:35:00"),
#     (90, "L&T Technology Services Ltd", "Engineering and R&D services company", "2020-07-27 09:55:00"),

#     (91, "Suzlon Energy Ltd", "Wind turbine manufacturing and renewable energy company", "2019-02-11 10:30:00"),
#     (92, "ReNew Power Ltd", "Renewable energy generation company", "2021-05-03 11:45:00"),
#     (93, "NHPC Ltd", "Hydroelectric power generation company", "2018-12-22 09:10:00"),

#     (94, "ONGC Petro Additions Ltd", "Petrochemical manufacturing company", "2020-01-15 14:00:00"),
#     (95, "Mangalore Refinery and Petrochemicals Ltd", "Oil refining and petrochemical manufacturing company", "2019-04-08 10:20:00"),

#     (96, "Ashok Leyland Defence Systems", "Defense vehicle manufacturing company", "2021-06-11 15:05:00"),
#     (97, "Bharat Electronics Ltd", "Defense electronics manufacturing company", "2018-10-19 09:25:00"),
#     (98, "Hindustan Aeronautics Ltd", "Aerospace and defense manufacturing company", "2019-01-04 11:50:00"),

#     (99, "CESC Ltd", "Electric power generation and distribution company", "2020-09-09 10:40:00"),
#     (100, "Tata Advanced Systems Ltd", "Defense and aerospace manufacturing company", "2022-08-16 14:10:00"),

#     (101, "Indian Railway Finance Corporation", "Railway infrastructure financing company", "2021-03-30 09:00:00"),
#     (102, "Rail Vikas Nigam Ltd", "Railway infrastructure development company", "2019-06-25 11:15:00"),
#     (103, "Mazagon Dock Shipbuilders Ltd", "Shipbuilding and defense manufacturing company", "2020-10-12 13:45:00"),
#     (104, "Cochin Shipyard Ltd", "Shipbuilding and ship repair company", "2019-07-04 10:30:00"),
#     (105, "Garden Reach Shipbuilders", "Defense shipbuilding company", "2021-01-18 14:20:00"),
#     (106, "IRCON International Ltd", "Infrastructure construction and engineering company", "2020-02-22 11:40:00"),
#     (107, "NBCC (India) Ltd", "Construction and real estate development company", "2019-11-09 09:50:00"),
#     (108, "Engineers India Ltd", "Engineering consultancy and project management company", "2021-04-26 10:15:00"),
#     (109, "National Aluminium Company Ltd", "Integrated aluminium manufacturing company", "2018-08-30 09:30:00"),
#     (110, "Balmer Lawrie & Co Ltd", "Industrial packaging and logistics services company", "2020-05-13 11:00:00"),

#     (111, "RITES Ltd", "Transport infrastructure consultancy company", "2019-03-18 10:40:00"),
#     (112, "IRFC Ltd", "Railway project financing company", "2021-02-01 09:10:00"),
#     (113, "HUDCO Ltd", "Housing and urban infrastructure finance company", "2020-01-28 14:30:00"),
#     (114, "Power Finance Corporation Ltd", "Power sector financing company", "2019-09-06 11:25:00"),
#     (115, "REC Limited", "Power infrastructure financing company", "2021-07-09 15:00:00"),
#     (116, "NLC India Ltd", "Lignite mining and power generation company", "2018-12-10 10:20:00"),
#     (117, "SJVN Ltd", "Hydro and renewable power generation company", "2020-06-01 09:35:00"),
#     (118, "IIFL Finance Ltd", "Financial services and investment company", "2022-02-07 11:10:00"),
#     (119, "Muthoot Finance Ltd", "Gold loan and financial services company", "2021-08-13 10:45:00"),
#     (120, "Manappuram Finance Ltd", "Gold loan and microfinance services provider", "2020-03-19 14:55:00"),

#     (121, "Federal Bank Ltd", "Private sector commercial bank", "2019-07-15 09:30:00"),
#     (122, "South Indian Bank Ltd", "Private sector bank offering retail banking services", "2021-01-21 11:50:00"),
#     (123, "IDFC First Bank Ltd", "Private sector universal bank", "2022-06-03 10:15:00"),
#     (124, "Bandhan Bank Ltd", "Retail-focused commercial bank", "2020-10-14 14:35:00"),
#     (125, "Yes Bank Ltd", "Private sector bank providing corporate banking services", "2019-04-02 09:00:00"),
#     (126, "RBL Bank Ltd", "Private sector scheduled commercial bank", "2021-11-29 13:40:00"),
#     (127, "Ujjivan Small Finance Bank", "Small finance bank focused on financial inclusion", "2020-02-17 10:30:00"),
#     (128, "Equitas Small Finance Bank", "Retail and MSME focused small finance bank", "2021-05-06 11:45:00"),
#     (129, "CSB Bank Ltd", "Private sector bank offering retail and SME banking", "2019-08-09 09:20:00"),
#     (130, "AU Small Finance Bank", "Retail banking and lending services provider", "2022-03-11 14:00:00"),

#     (131, "JSW Infrastructure Ltd", "Port and logistics infrastructure company", "2021-09-20 10:10:00"),
#     (132, "Adani Wilmar Ltd", "Edible oil and food processing company", "2022-01-27 11:30:00"),
#     (133, "Tata Autocomp Systems Ltd", "Automotive component manufacturing company", "2020-05-18 09:55:00"),
#     (134, "Endurance Technologies Ltd", "Automotive component manufacturer", "2019-10-07 14:25:00"),
#     (135, "UNO Minda Ltd", "Automotive components and systems manufacturer", "2021-06-24 10:40:00"),
#     (136, "Schaeffler India Ltd", "Automotive and industrial component manufacturer", "2020-11-16 13:15:00"),
#     (137, "ZF Commercial Vehicle Control Systems", "Commercial vehicle systems manufacturing company", "2022-04-14 11:05:00"),
#     (138, "Bosch Chassis Systems India", "Automotive safety systems manufacturing company", "2019-12-04 09:45:00"),
#     (139, "MRF Ltd", "Tyre manufacturing company", "2018-08-21 10:30:00"),
#     (140, "CEAT Ltd", "Tyre manufacturing company", "2021-07-29 15:20:00"),

#     (141, "JK Tyre & Industries Ltd", "Tyre and rubber products manufacturing company", "2020-03-09 11:10:00"),
#     (142, "Apollo Tyres Ltd", "Tyre manufacturing and distribution company", "2019-06-13 09:30:00"),
#     (143, "Exide Industries Ltd", "Battery manufacturing and energy storage company", "2021-02-04 10:50:00"),
#     (144, "Amara Raja Energy & Mobility", "Battery and energy storage solutions company", "2022-08-25 14:15:00"),
#     (145, "Hindustan Zinc Ltd", "Zinc and lead mining company", "2019-01-30 09:20:00"),
#     (146, "NMDC Steel Ltd", "Steel manufacturing and mining company", "2021-12-18 11:35:00"),
#     (147, "APL Apollo Tubes Ltd", "Structural steel tube manufacturing company", "2020-10-06 10:05:00"),
#     (148, "Ramco Industries Ltd", "Building materials and fiber cement products company", "2019-05-27 14:40:00"),
#     (149, "Ramco Cements Ltd", "Cement manufacturing company", "2021-09-01 11:25:00"),
#     (150, "Dalmia Bharat Ltd", "Cement manufacturing and sustainability-focused company", "2022-02-28 15:00:00")
# ]

EMISSION_EQUIPMENT_TYPES = [
    (1, "Boiler", "Industrial boiler for steam generation"),
    (2, "Diesel Generator", "Diesel-based power backup generator"),
    (3, "Gas Turbine", "Gas turbine for power generation"),
    (4, "Steam Turbine", "Steam turbine for electricity generation"),
    (5, "Furnace", "Industrial furnace for material processing"),
    (6, "Kiln", "Rotary kiln used in cement manufacturing"),
    (7, "Compressor", "Gas compression equipment"),
    (8, "Heater", "Process heater for temperature control"),
    (9, "Incinerator", "Waste incineration equipment"),
    (10, "Flare Stack", "Gas flaring equipment"),
    (11, "Internal Combustion Engine", "IC engine used in industrial operations"),
    (12, "Coal Fired Boiler", "Boiler using coal as fuel"),
    (13, "Gas Fired Boiler", "Boiler using natural gas as fuel"),
    (14, "Oil Fired Boiler", "Boiler using furnace oil"),
    (15, "Thermal Oxidizer", "VOC destruction equipment"),
    (16, "Heat Recovery Steam Generator", "Heat recovery unit in power plants"),
    (17, "Power Generator", "Electric power generation equipment"),
    (18, "Air Compressor", "Compressed air generation system"),
    (19, "Process Pump", "Pump for fluid movement"),
    (20, "Material Dryer", "Dryer used in manufacturing processes"),
    (21, "Calciner", "Calcination equipment for cement"),
    (22, "Melting Furnace", "Metal melting furnace"),
    (23, "Annealing Furnace", "Heat treatment furnace"),
    (24, "Cracking Furnace", "Hydrocarbon cracking equipment"),
    (25, "Hydrogen Reformer", "Hydrogen production equipment"),
    (26, "Gas Engine", "Natural gas engine"),
    (27, "Oil Engine", "Oil-powered internal engine"),
    (28, "Power Boiler", "High-pressure industrial boiler"),
    (29, "Process Kiln", "Kiln for industrial processing"),
    (30, "Vacuum Distillation Unit", "Refinery distillation unit"),
    (31, "Atmospheric Distillation Unit", "Primary refinery processing unit"),
    (32, "Catalytic Cracker", "Fluid catalytic cracking unit"),
    (33, "Hydrotreater", "Hydrocarbon treatment equipment"),
    (34, "Reformer Unit", "Catalytic reforming equipment"),
    (35, "Coke Oven", "Coke production oven"),
    (36, "Blast Furnace", "Iron smelting furnace"),
    (37, "Electric Arc Furnace", "Steel melting furnace"),
    (38, "Rolling Mill Heater", "Steel rolling mill heater"),
    (39, "Sinter Plant", "Sintering plant equipment"),
    (40, "Pellet Plant", "Iron ore pelletizing unit"),
    (41, "Mining Excavator", "Diesel-powered mining excavator"),
    (42, "Mining Haul Truck", "Heavy-duty mining transport truck"),
    (43, "Stacker Reclaimer", "Bulk material handling equipment"),
    (44, "Port Crane", "Diesel-powered port crane"),
    (45, "Ship Loader", "Bulk cargo loading equipment"),
    (46, "Container Handler", "Container lifting equipment"),
    (47, "Forklift", "Diesel-powered forklift"),
    (48, "Reach Stacker", "Container handling vehicle"),
    (49, "Emergency Generator", "Backup generator for emergencies"),
    (50, "Data Center Generator", "Generator supporting data center operations")
]

FACILITY_TYPES_MASTER = [
    (1, "Manufacturing Plant", "Industrial manufacturing and processing facility"),
    (2, "Corporate Office", "Administrative and corporate operations facility"),
    (3, "Warehouse", "Storage and logistics facility"),
    (4, "Refinery", "Oil and gas refining and processing facility"),
    (5, "Power Plant", "Thermal or renewable power generation facility"),
    (6, "Port Terminal", "Port and cargo handling infrastructure"),
    (7, "Data Center", "IT infrastructure and data processing facility"),
    (8, "Mining Site", "Mineral extraction and mining operations"),
    (9, "R&D Center", "Research and development facility"),
    (10, "Distribution Center", "Product distribution and supply chain hub")
]


FACILITY_TYPE_DATA = {
    1: {
        "names": ["Manufacturing Plant", "Production Unit", "Industrial Facility"],
        "locations": ["Pune, Maharashtra", "Coimbatore, Tamil Nadu", "Ahmedabad, Gujarat"]
    },
    2: {
        "names": ["Corporate Office", "Regional Office", "IT Campus"],
        "locations": ["Bengaluru, Karnataka", "Hyderabad, Telangana", "Chennai, Tamil Nadu"]
    },
    3: {
        "names": ["Central Warehouse", "Logistics Hub", "Storage Facility"],
        "locations": ["Nagpur, Maharashtra", "Bhiwandi, Maharashtra", "Noida, Uttar Pradesh"]
    },
    4: {
        "names": ["Oil Refinery", "Gas Processing Complex", "Petroleum Refinery"],
        "locations": ["Jamnagar, Gujarat", "Panipat, Haryana", "Kochi, Kerala"]
    },
    5: {
        "names": ["Thermal Power Plant", "Gas Power Station", "Renewable Power Plant"],
        "locations": ["Singrauli, Madhya Pradesh", "Ramagundam, Telangana", "Mundra, Gujarat"]
    },
    6: {
        "names": ["Port Terminal", "Cargo Port", "Container Terminal"],
        "locations": ["Mundra, Gujarat", "Nhava Sheva, Maharashtra", "Visakhapatnam, Andhra Pradesh"]
    },
    7: {
        "names": ["Primary Data Center", "Disaster Recovery Data Center", "Cloud Data Center"],
        "locations": ["Mumbai, Maharashtra", "Chennai, Tamil Nadu", "Hyderabad, Telangana"]
    },
    8: {
        "names": ["Open Cast Mine", "Underground Mine", "Mining Site"],
        "locations": ["Dhanbad, Jharkhand", "Bellary, Karnataka", "Korba, Chhattisgarh"]
    },
    9: {
        "names": ["R&D Center", "Innovation Lab", "Technology Research Center"],
        "locations": ["Bengaluru, Karnataka", "Pune, Maharashtra", "Noida, Uttar Pradesh"]
    },
    10: {
        "names": ["Distribution Center", "Supply Chain Hub", "Regional Distribution Center"],
        "locations": ["Gurugram, Haryana", "Indore, Madhya Pradesh", "Vijayawada, Andhra Pradesh"]
    }
}

GAS_TYPES_MASTER = [
    (1, "Carbon Dioxide (CO2)", "kg"),
    (2, "Methane (CH4)", "kg"),
    (3, "Nitrous Oxide (N2O)", "kg"),
    (4, "Carbon Monoxide (CO)", "kg"),
    (5, "Sulfur Dioxide (SO2)", "kg"),
    (6, "Nitrogen Oxides (NOx)", "kg"),
    (7, "Nitric Oxide (NO)", "kg"),
    (8, "Nitrogen Dioxide (NO2)", "kg"),
    (9, "Ammonia (NH3)", "kg"),
    (10, "Hydrogen Sulfide (H2S)", "kg"),

    (11, "Volatile Organic Compounds (VOC)", "kg"),
    (12, "Non-Methane VOC (NMVOC)", "kg"),
    (13, "Particulate Matter (PM)", "kg"),
    (14, "PM10", "kg"),
    (15, "PM2.5", "kg"),

    (16, "Hydrofluorocarbon-23 (HFC-23)", "kg"),
    (17, "Hydrofluorocarbon-134a (HFC-134a)", "kg"),
    (18, "Hydrofluorocarbon-125 (HFC-125)", "kg"),
    (19, "Perfluoromethane (CF4)", "kg"),
    (20, "Perfluoroethane (C2F6)", "kg"),

    (21, "Sulfur Hexafluoride (SF6)", "kg"),
    (22, "Nitrogen Trifluoride (NF3)", "kg"),
    (23, "Trifluoromethane (CHF3)", "kg"),
    (24, "Dinitrogen Tetroxide (N2O4)", "kg"),
    (25, "Ozone (O3)", "kg"),

    (26, "Hydrogen (H2)", "kg"),
    (27, "Oxygen (O2)", "kg"),
    (28, "Argon (Ar)", "kg"),
    (29, "Helium (He)", "kg"),
    (30, "Neon (Ne)", "kg"),

    (31, "Propane (C3H8)", "kg"),
    (32, "Butane (C4H10)", "kg"),
    (33, "Ethane (C2H6)", "kg"),
    (34, "Ethylene (C2H4)", "kg"),
    (35, "Acetylene (C2H2)", "kg"),

    (36, "Sulfur Trioxide (SO3)", "kg"),
    (37, "Chlorine (Cl2)", "kg"),
    (38, "Hydrogen Chloride (HCl)", "kg"),
    (39, "Hydrogen Fluoride (HF)", "kg"),
    (40, "Carbon Tetrachloride (CCl4)", "kg"),

    (41, "Trichlorofluoromethane (CFC-11)", "kg"),
    (42, "Dichlorodifluoromethane (CFC-12)", "kg"),
    (43, "Trichlorotrifluoroethane (CFC-113)", "kg"),
    (44, "Bromotrifluoromethane (Halon-1301)", "kg"),
    (45, "Bromochlorodifluoromethane (Halon-1211)", "kg"),

    (46, "Isopropyl Alcohol Vapors", "kg"),
    (47, "Methanol Vapors", "kg"),
    (48, "Ethanol Vapors", "kg"),
    (49, "Formaldehyde", "kg"),
    (50, "Acrolein", "kg")
]




FUEL_TYPES_MASTER = [
    (1, "Diesel", "Liters"),
    (2, "Petrol", "Liters"),
    (3, "Natural Gas", "SCM"),
    (4, "Liquefied Natural Gas (LNG)", "kg"),
    (5, "Compressed Natural Gas (CNG)", "kg"),
    (6, "Furnace Oil", "Liters"),
    (7, "Light Diesel Oil (LDO)", "Liters"),
    (8, "Heavy Fuel Oil (HFO)", "Liters"),
    (9, "Kerosene", "Liters"),
    (10, "Coal", "MT"),

    (11, "Lignite", "MT"),
    (12, "Coke", "MT"),
    (13, "Petroleum Coke (Pet Coke)", "MT"),
    (14, "Bituminous Coal", "MT"),
    (15, "Anthracite Coal", "MT"),

    (16, "Biomass Pellets", "MT"),
    (17, "Bagasse", "MT"),
    (18, "Wood Chips", "MT"),
    (19, "Rice Husk", "MT"),
    (20, "Agricultural Waste", "MT"),

    (21, "Methanol", "Liters"),
    (22, "Ethanol", "Liters"),
    (23, "Bio-Diesel", "Liters"),
    (24, "Bio-Ethanol", "Liters"),
    (25, "Synthetic Gas", "SCM"),

    (26, "Propane", "kg"),
    (27, "Butane", "kg"),
    (28, "Liquefied Petroleum Gas (LPG)", "kg"),
    (29, "Aviation Turbine Fuel (ATF)", "Liters"),
    (30, "Marine Fuel Oil", "Liters"),

    (31, "Gas Oil", "Liters"),
    (32, "Residual Fuel Oil", "Liters"),
    (33, "Naptha", "Liters"),
    (34, "Refinery Gas", "SCM"),
    (35, "Blast Furnace Gas", "SCM"),

    (36, "Coke Oven Gas", "SCM"),
    (37, "Producer Gas", "SCM"),
    (38, "Town Gas", "SCM"),
    (39, "Hydrogen Fuel", "kg"),
    (40, "Ammonia Fuel", "kg"),

    (41, "Solar Thermal Backup Fuel", "Liters"),
    (42, "Wind Generator Backup Diesel", "Liters"),
    (43, "Waste Oil", "Liters"),
    (44, "Used Lubricant Oil", "Liters"),
    (45, "Pyrolysis Oil", "Liters"),

    (46, "Municipal Solid Waste (MSW)", "MT"),
    (47, "Refuse Derived Fuel (RDF)", "MT"),
    (48, "Tyre Derived Fuel (TDF)", "MT"),
    (49, "Plastic Waste Fuel", "MT"),
    (50, "Industrial Solvent Fuel", "Liters")
]

EQUIPMENT_FUEL_MAP = {

    # --- BOILERS ---
    "Boiler":                           ["Coal", "Natural Gas", "Furnace Oil", "Biomass Pellets", "Light Diesel Oil (LDO)"],
    "Coal Fired Boiler":                ["Coal", "Bituminous Coal", "Lignite", "Petroleum Coke (Pet Coke)"],
    "Gas Fired Boiler":                 ["Natural Gas", "Liquefied Natural Gas (LNG)", "Compressed Natural Gas (CNG)"],
    "Oil Fired Boiler":                 ["Furnace Oil", "Heavy Fuel Oil (HFO)", "Light Diesel Oil (LDO)", "Residual Fuel Oil"],
    "Power Boiler":                     ["Coal", "Furnace Oil", "Natural Gas", "Bituminous Coal"],

    # --- TURBINES & GENERATORS ---
    "Gas Turbine":                      ["Natural Gas", "Liquefied Natural Gas (LNG)", "Refinery Gas", "Synthetic Gas"],
    "Steam Turbine":                    ["Coal", "Natural Gas", "Furnace Oil", "Biomass Pellets"],
    "Power Generator":                  ["Diesel", "Natural Gas", "Heavy Fuel Oil (HFO)", "Liquefied Petroleum Gas (LPG)"],
    "Diesel Generator":                 ["Diesel", "Bio-Diesel", "Light Diesel Oil (LDO)"],
    "Emergency Generator":              ["Diesel", "Light Diesel Oil (LDO)"],
    "Data Center Generator":            ["Diesel", "Natural Gas"],
    "Heat Recovery Steam Generator":    ["Natural Gas", "Refinery Gas", "Diesel"],

    # --- ENGINES ---
    "Gas Engine":                       ["Natural Gas", "Compressed Natural Gas (CNG)", "Liquefied Natural Gas (LNG)", "Synthetic Gas"],
    "Oil Engine":                       ["Furnace Oil", "Heavy Fuel Oil (HFO)", "Light Diesel Oil (LDO)", "Diesel"],
    "Internal Combustion Engine":       ["Diesel", "Petrol", "Compressed Natural Gas (CNG)", "Liquefied Petroleum Gas (LPG)"],

    # --- FURNACES ---
    "Furnace":                          ["Coal", "Natural Gas", "Furnace Oil", "Coke", "Producer Gas"],
    "Melting Furnace":                  ["Natural Gas", "Furnace Oil", "Coke", "Coal", "Propane"],
    "Annealing Furnace":                ["Natural Gas", "Furnace Oil", "Liquefied Petroleum Gas (LPG)"],
    "Cracking Furnace":                 ["Refinery Gas", "Natural Gas", "Naptha"],
    "Blast Furnace":                    ["Coke", "Blast Furnace Gas", "Coal", "Bituminous Coal"],

    # --- KILNS ---
    "Kiln":                             ["Coal", "Petroleum Coke (Pet Coke)", "Natural Gas", "Biomass Pellets"],
    "Process Kiln":                     ["Coal", "Natural Gas", "Petroleum Coke (Pet Coke)", "Light Diesel Oil (LDO)"],
    "Calciner":                         ["Coal", "Petroleum Coke (Pet Coke)", "Natural Gas", "Coke Oven Gas"],

    # --- REFINERY UNITS ---
    "Vacuum Distillation Unit":         ["Refinery Gas", "Natural Gas", "Furnace Oil"],
    "Atmospheric Distillation Unit":    ["Refinery Gas", "Natural Gas", "Furnace Oil"],
    "Catalytic Cracker":                ["Refinery Gas", "Natural Gas", "Coke"],
    "Hydrotreater":                     ["Refinery Gas", "Natural Gas", "Hydrogen Fuel"],
    "Reformer Unit":                    ["Natural Gas", "Refinery Gas", "Naptha"],
    "Hydrogen Reformer":                ["Natural Gas", "Refinery Gas", "Naptha"],
    "Coke Oven":                        ["Bituminous Coal", "Coke Oven Gas", "Coal"],

    # --- STEEL / METAL ---
    "Electric Arc Furnace":             ["Coke Oven Gas", "Natural Gas", "Propane"],
    "Rolling Mill Heater":              ["Natural Gas", "Coke Oven Gas", "Furnace Oil", "Light Diesel Oil (LDO)"],
    "Sinter Plant":                     ["Coke", "Coal", "Coke Oven Gas", "Blast Furnace Gas"],
    "Pellet Plant":                     ["Coal", "Natural Gas", "Light Diesel Oil (LDO)"],

    # --- PROCESS / INDUSTRIAL ---
    "Compressor":                       ["Natural Gas", "Diesel", "Compressed Natural Gas (CNG)"],
    "Heater":                           ["Natural Gas", "Furnace Oil", "Liquefied Petroleum Gas (LPG)", "Diesel"],
    "Incinerator":                      ["Diesel", "Natural Gas", "Municipal Solid Waste (MSW)", "Refuse Derived Fuel (RDF)", "Industrial Solvent Fuel"],
    "Flare Stack":                      ["Natural Gas", "Refinery Gas", "Coke Oven Gas", "Blast Furnace Gas"],
    "Thermal Oxidizer":                 ["Natural Gas", "Diesel", "Liquefied Petroleum Gas (LPG)"],
    "Air Compressor":                   ["Diesel", "Natural Gas", "Compressed Natural Gas (CNG)"],
    "Process Pump":                     ["Diesel", "Natural Gas", "Compressed Natural Gas (CNG)"],
    "Material Dryer":                   ["Natural Gas", "Coal", "Furnace Oil", "Biomass Pellets", "Light Diesel Oil (LDO)"],

    # --- MINING ---
    "Mining Excavator":                 ["Diesel", "Bio-Diesel"],
    "Mining Haul Truck":                ["Diesel", "Bio-Diesel", "Compressed Natural Gas (CNG)"],
    "Stacker Reclaimer":                ["Diesel", "Light Diesel Oil (LDO)"],

    # --- PORT / LOGISTICS ---
    "Port Crane":                       ["Diesel", "Heavy Fuel Oil (HFO)", "Marine Fuel Oil"],
    "Ship Loader":                      ["Diesel", "Heavy Fuel Oil (HFO)"],
    "Container Handler":                ["Diesel", "Liquefied Petroleum Gas (LPG)"],
    "Forklift":                         ["Diesel", "Liquefied Petroleum Gas (LPG)", "Compressed Natural Gas (CNG)"],
    "Reach Stacker":                    ["Diesel", "Liquefied Petroleum Gas (LPG)"],
}


# =========================
# STANDARD (REAL ESG VALUES)
# =========================
STANDARDS = [
    (
        1,
        "GHG Protocol – Corporate Standard",
        "World Resources Institute (WRI) & World Business Council for Sustainable Development (WBCSD)",
        "Revised Edition 2015",
        "Global standard for corporate greenhouse gas accounting"
    ),
    (
        2,
        "ISO 14064-1",
        "International Organization for Standardization (ISO)",
        "2018",
        "Specification for quantification and reporting of GHG emissions"
    ),
    (
        3,
        "ISO 14067",
        "International Organization for Standardization (ISO)",
        "2018",
        "Carbon footprint of products standard"
    ),
    (
        4,
        "IPCC Guidelines for National GHG Inventories",
        "Intergovernmental Panel on Climate Change (IPCC)",
        "2006 + 2019 Refinement",
        "Methodologies for estimating national greenhouse gas inventories"
    ),
    (
        5,
        "Science Based Targets initiative (SBTi)",
        "Science Based Targets initiative",
        "2021",
        "Guidance for setting science-based emissions reduction targets"
    )
]




# =========================
# CALCULATION METHOD MASTER
# =========================
CALCULATION_METHODS = [


    # --- GHGs ---
    (1, "CO2 Fuel Combustion Method",
     "Emissions = Fuel_Consumed × CO2_Emission_Factor",
     1, 1, "kg CO2"),


    (2, "CH4 Fuel Combustion Method",
     "Emissions = Fuel_Consumed × CH4_Emission_Factor",
     1, 2, "kg CH4"),


    (3, "N2O Fuel Combustion Method",
     "Emissions = Fuel_Consumed × N2O_Emission_Factor",
     1, 3, "kg N2O"),


    # --- Air Pollutants ---
    (4, "CO Emission Calculation",
     "Emissions = Activity_Data × CO_Factor",
     4, 4, "kg"),


    (5, "SO2 Emission Calculation",
     "Emissions = Activity_Data × SO2_Factor",
     4, 5, "kg"),


    (6, "NOx Emission Calculation",
     "Emissions = Activity_Data × NOx_Factor",
     4, 6, "kg"),


    (7, "NO Emission Calculation",
     "Emissions = Activity_Data × NO_Factor",
     4, 7, "kg"),


    (8, "NO2 Emission Calculation",
     "Emissions = Activity_Data × NO2_Factor",
     4, 8, "kg"),


    (9, "NH3 Emission Calculation",
     "Emissions = Activity_Data × NH3_Factor",
     4, 9, "kg"),


    (10, "H2S Emission Calculation",
     "Emissions = Activity_Data × H2S_Factor",
     4, 10, "kg"),


    # --- VOCs ---
    (11, "VOC Emission Estimation",
     "Emissions = Solvent_Used × VOC_Factor",
     4, 11, "kg"),


    (12, "NMVOC Emission Estimation",
     "Emissions = Solvent_Used × NMVOC_Factor",
     4, 12, "kg"),


    # --- Particulates ---
    (13, "PM Emission Calculation",
     "Emissions = Activity × PM_Factor",
     4, 13, "kg"),


    (14, "PM10 Emission Calculation",
     "Emissions = Activity × PM10_Factor",
     4, 14, "kg"),


    (15, "PM2.5 Emission Calculation",
     "Emissions = Activity × PM2.5_Factor",
     4, 15, "kg"),


    # --- F-Gases / ODS ---
    (16, "HFC Leakage Method",
     "Emissions = Refrigerant_Charge × Leakage_Rate",
     3, 16, "kg"),


    (17, "Perfluorocarbon Emission Method",
     "Emissions = Charge × Emission_Factor",
     3, 19, "kg"),


    (18, "SF6 Equipment Leakage Method",
     "Emissions = Installed_Capacity × Leakage_Rate",
     3, 21, "kg"),


    (19, "NF3 Semiconductor Method",
     "Emissions = Consumption × EF",
     3, 22, "kg"),


    # --- Process / Inert Gases ---
    (20, "Process Gas Release Method",
     "Emissions = Released_Quantity",
     2, 26, "kg"),


    # --- Fuel Gases ---
    (21, "Fuel Gas Combustion Method",
     "Emissions = Fuel_Consumed × EF",
     1, 31, "kg"),


    # --- Toxic / Chemical Vapors ---
    (22, "Chemical Vapor Emission Method",
     "Emissions = Usage × Vaporization_Factor",
     4, 46, "kg"),


    (23, "Alcohol Vapor Emission Method",
     "Emissions = Consumption × EF",
     4, 47, "kg"),


    (24, "Formaldehyde Emission Method",
     "Emissions = Activity × HCHO_Factor",
     4, 49, "kg"),


    (25, "Acrolein Emission Method",
     "Emissions = Activity × Acrolein_Factor",
     4, 50, "kg"),
]



