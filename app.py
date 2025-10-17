import streamlit as st
import pandas as pd

# Grading system mapping
GRADING_SYSTEM = {
    'A': {'range': (85, 100), 'points': 4.0},
    'A-': {'range': (80, 84), 'points': 3.7},
    'B+': {'range': (75, 79), 'points': 3.3},
    'B': {'range': (70, 74), 'points': 3.0},
    'B-': {'range': (65, 69), 'points': 2.7},
    'C+': {'range': (61, 64), 'points': 2.3},
    'C': {'range': (58, 60), 'points': 2.0},
    'C-': {'range': (55, 57), 'points': 1.7},
    'D': {'range': (50, 54), 'points': 1.0},
    'F': {'range': (0, 49), 'points': 0.0}
}

def get_grade_and_points(marks):
    """Convert marks to grade and grade points"""
    for grade, info in GRADING_SYSTEM.items():
        min_range, max_range = info['range']
        if min_range <= marks <= max_range:
            return grade, info['points']
    return 'F', 0.0

def calculate_gpa(subjects_data):
    """Calculate GPA from subjects data"""
    total_points = 0
    total_credits = 0
    
    for subject in subjects_data:
        credits = subject['credits']
        grade_points = subject['grade_points']
        total_points += credits * grade_points
        total_credits += credits
    
    return total_points / total_credits if total_credits > 0 else 0

def main():
    st.set_page_config(
        page_title="GPA & CGPA Calculator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🎓 GPA & CGPA Calculator")
    st.markdown("Calculate your GPA and CGPA according to the DS Grading System")
    
    # Display grading system
    with st.expander("📋 Grading System Reference"):
        st.write("""
        **Grading Scale:**
        - A: 85-100% (4.0)
        - A-: 80-84% (3.7)
        - B+: 75-79% (3.3)
        - B: 70-74% (3.0)
        - B-: 65-69% (2.7)
        - C+: 61-64% (2.3)
        - C: 58-60% (2.0)
        - C-: 55-57% (1.7)
        - D: 50-54% (1.0)
        - F: Below 50% (0.0)
        """)
    
    # Main tabs
    tab1, tab2 = st.tabs(["📚 GPA Calculator", "🏆 CGPA Calculator"])
    
    with tab1:
        st.header("Semester GPA Calculator")
        
        # Number of subjects input
        num_subjects = st.number_input(
            "Number of Subjects:",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            key="gpa_subjects_count"
        )
        
        subjects_data = []
        
        # Create input fields for each subject
        st.subheader("Enter Subject Details")
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write("**Subject Name**")
        with col2:
            st.write("**Marks (%)**")
        with col3:
            st.write("**Credits**")
        
        for i in range(num_subjects):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                subject_name = st.text_input(
                    f"Subject {i+1}",
                    value=f"Subject {i+1}",
                    key=f"subject_name_{i}"
                )
            
            with col2:
                marks = st.number_input(
                    "Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=75.0,
                    step=0.5,
                    key=f"marks_{i}"
                )
            
            with col3:
                credits = st.number_input(
                    "Credits",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"credits_{i}"
                )
            
            # Calculate grade and points
            grade, points = get_grade_and_points(marks)
            
            subjects_data.append({
                'name': subject_name,
                'marks': marks,
                'credits': credits,
                'grade': grade,
                'grade_points': points
            })
        
        # Calculate and display results
        if st.button("Calculate GPA", key="calculate_gpa"):
            gpa = calculate_gpa(subjects_data)
            
            # Display results in a nice format
            st.success(f"**Your GPA: {gpa:.2f}**")
            
            # Show detailed results table
            st.subheader("Detailed Results")
            results_df = pd.DataFrame(subjects_data)
            results_df = results_df[['name', 'marks', 'credits', 'grade', 'grade_points']]
            st.dataframe(results_df, use_container_width=True)
            
            # Show calculation breakdown
            st.subheader("Calculation Breakdown")
            total_credits = sum(subject['credits'] for subject in subjects_data)
            total_points = sum(subject['credits'] * subject['grade_points'] for subject in subjects_data)
            
            st.write(f"Total Credits: {total_credits}")
            st.write(f"Total Grade Points: {total_points:.2f}")
            st.write(f"GPA = Total Grade Points / Total Credits = {total_points:.2f} / {total_credits} = {gpa:.2f}")
    
    with tab2:
        st.header("Cumulative CGPA Calculator")
        
        num_semesters = st.number_input(
            "Number of Semesters:",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
            key="cgpa_semesters_count"
        )
        
        semesters_data = []
        
        for sem in range(num_semesters):
            st.subheader(f"Semester {sem + 1}")
            
            num_subjects_sem = st.number_input(
                f"Number of Subjects in Semester {sem + 1}:",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
                key=f"sem_{sem}_subjects"
            )
            
            sem_subjects = []
            
            for i in range(num_subjects_sem):
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    subject_name = st.text_input(
                        f"Sem {sem+1} Subject {i+1}",
                        value=f"Subject {i+1}",
                        key=f"sem{sem}_subject_name_{i}"
                    )
                
                with col2:
                    marks = st.number_input(
                        "Marks",
                        min_value=0.0,
                        max_value=100.0,
                        value=75.0,
                        step=0.5,
                        key=f"sem{sem}_marks_{i}"
                    )
                
                with col3:
                    credits = st.number_input(
                        "Credits",
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        key=f"sem{sem}_credits_{i}"
                    )
                
                grade, points = get_grade_and_points(marks)
                
                sem_subjects.append({
                    'name': subject_name,
                    'marks': marks,
                    'credits': credits,
                    'grade': grade,
                    'grade_points': points
                })
            
            sem_gpa = calculate_gpa(sem_subjects)
            sem_credits = sum(subject['credits'] for subject in sem_subjects)
            
            semesters_data.append({
                'semester': sem + 1,
                'subjects': sem_subjects,
                'gpa': sem_gpa,
                'total_credits': sem_credits
            })
        
        if st.button("Calculate CGPA", key="calculate_cgpa"):
            total_cumulative_points = 0
            total_cumulative_credits = 0
            
            st.subheader("Semester-wise Results")
            sem_results = []
            
            for sem in semesters_data:
                sem_points = sem['gpa'] * sem['total_credits']
                total_cumulative_points += sem_points
                total_cumulative_credits += sem['total_credits']
                
                sem_results.append({
                    'Semester': sem['semester'],
                    'GPA': f"{sem['gpa']:.2f}",
                    'Total Credits': sem['total_credits'],
                    'Total Points': f"{sem_points:.2f}"
                })
            
            # Display semester results
            sem_df = pd.DataFrame(sem_results)
            st.dataframe(sem_df, use_container_width=True)
            
            # Calculate and display CGPA
            cgpa = total_cumulative_points / total_cumulative_credits if total_cumulative_credits > 0 else 0
            
            st.success(f"**Your CGPA: {cgpa:.2f}**")
            
            # Show CGPA calculation breakdown
            st.subheader("CGPA Calculation Breakdown")
            st.write(f"Total Cumulative Points: {total_cumulative_points:.2f}")
            st.write(f"Total Cumulative Credits: {total_cumulative_credits}")
            st.write(f"CGPA = Total Cumulative Points / Total Cumulative Credits")
            st.write(f"CGPA = {total_cumulative_points:.2f} / {total_cumulative_credits} = {cgpa:.2f}")

    # Footer
    st.markdown("---")
    st.markdown(
        "**Note:** This calculator uses the DS Grading System. "
        "Make sure to enter marks between 0-100 and appropriate credit hours for each subject."
    )

if __name__ == "__main__":
    main()
