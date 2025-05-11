"""
Flask Web App: Student Marks Averaging Tool

This app allows users to input marks for:
- Two MID exams (each out of 20)
- Five class test/assignment scores (each out of 10)

Features:
- Input validation using HTML form constraints
- Selects the best 3 out of 5 class test marks
- Calculates:
    1. Average of MID marks
    2. Average of best 3 class tests
    3. Final weighted average (80% of higher MID + 20% of lower + test average)

"""
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            mid1 = float(request.form.get('mid1'))
            mid2 = float(request.form.get('mid2'))
            tests = [float(request.form[f'test{i}']) for i in range(1, 6)]

            # Validation
            if not (0 <= mid1 <= 20 and 0 <= mid2 <= 20):
                raise ValueError("MID marks must be between 0 and 20.")
            if not all(0 <= mark <= 10 for mark in tests):
                raise ValueError("All class test marks must be between 0 and 10.")

            # Calculations
            best_three = sorted(tests, reverse=True)[:3]
            avg_tests = sum(best_three) / 3
            weighted_mid = mid1 * 0.8 + mid2 * 0.2 if mid1 > mid2 else mid1 * 0.2 + mid2 * 0.8
            total_avg = weighted_mid + avg_tests
            mid_avg = (mid1 + mid2) / 2

            return render_template(
                'index.html',
                result={
                    'mid_avg': round(mid_avg, 2),
                    'total_avg': round(total_avg, 2),
                }
            )
        except ValueError as e:
            return render_template('index.html', error=str(e))
        except Exception:
            return render_template('index.html', error="Oops! Something went wrong. Try again.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
