def build_prompt(user_question):
    return f"""
You are an expert MySQL query generator.

Database: hospital_db

Tables:

patients:
- id
- gender (male/female)
- death_flag (1 = dead, 0 = alive)
- admitted (1 = admitted, 0 = not admitted)

RULES:
- 1 means TRUE, 0 means FALSE
- death_flag = 1 means patient died
- Always generate correct MySQL SQL
- Do not explain anything
- Return ONLY SQL query

Examples:

Q: How many patients died?
A: SELECT COUNT(*) FROM patients WHERE death_flag = 1;

Q: How many female patients died?
A: SELECT COUNT(*) FROM patients WHERE gender = 'female' AND death_flag = 1;

Q: What is mortality rate?
A: SELECT (SUM(death_flag)/COUNT(*))*100 AS mortality_rate FROM patients;

User Question:
{user_question}
"""