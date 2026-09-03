# E-Commerce Revenue Analysis 🛒

## Why I Built This

I've been learning SQL and Python for data analyst roles and 
wanted to go beyond just solving practice problems. I needed 
something real — a project where I actually had to think about 
business problems, not just write code.

So I built this end-to-end analysis to practice the full 
analyst workflow: loading messy data, cleaning it, finding 
patterns, and turning numbers into decisions a business 
can actually act on.

This is the kind of work I want to do every day as a data analyst.

---

## The Business Question

Simple: *Where is our revenue coming from, who are our best 
customers, and where are we losing money?*

---

## What I Found

The most surprising finding was about Premium customers. 
Despite being fewer in number, they drive significantly more 
revenue than Basic customers. And when I dug deeper — the 
top 2 revenue-generating products both belong to Fashion, 
which also has the highest profit margin (43%) compared to 
Grocery (19%).

So the story became clear: Premium customers buy Fashion. 
Fashion makes money. Grocery doesn't add much value and has 
the highest return rate on top of that.

The other finding that stood out — 19% of customers haven't 
purchased in over 60 days. That's nearly 1 in 5 customers 
silently walking away. That's a retention problem hiding in 
plain sight.

---

## What I Analyzed

- Monthly revenue trends — which months perform and which don't
- Customer segmentation — VIP, Regular, Occasional buyers
- Churn risk — customers inactive for 60+ days
- Product profitability — margin by category
- Return rate — which products are coming back and why
- Weekend vs weekday buying patterns

---

## The Hardest Part

Honestly, comparing customer behaviour against product 
performance at the same time was tricky. A product doing 
well doesn't always mean the customers buying it are loyal — 
and a customer segment being large doesn't mean they're 
profitable. Getting those two perspectives to tell one 
coherent story took the most thinking.

---

## What I'd Add Next

I want to go deeper on churn — right now I'm flagging 
customers as "at risk" but I want to predict *who* is 
likely to churn before they actually do.

I also want to understand the seasonality better. March 
is peak, May is low — but why? Is it a marketing thing, 
a product availability thing, or just consumer behaviour? 
That analysis would make the recommendations much stronger.

---

## Tools Used

- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Jupyter Notebook

---

## Files

- `analysis/ecommerce_analysis.py` — complete Python code
- `insights/business_insights.md` — recommendations for the business

---

## What This Project Taught Me

Data analysis is not about finding answers — it's about 
asking better questions. The numbers told me Fashion is 
doing well. But the real question is: *why are Premium 
customers gravitating toward Fashion, and how do we keep 
them there?*

That's the question I'd bring to a product or marketing 
team meeting.
