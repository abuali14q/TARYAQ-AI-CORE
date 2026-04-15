"""
📚 مثال استخدام مكتبة AI Analysis
Example usage of AI Analysis Library
"""

from ai_analysis import AIProjectAnalyzer

# ✅ إنشاء نموذج المحلل
analyzer = AIProjectAnalyzer()

# ✅ مثال 1: حساب التأخيرات المتقدم
print("=" * 60)
print("📊 مثال 1: حساب التأخيرات المتقدم")
print("=" * 60)

delay_analysis = analyzer.calculate_advanced_delay(
    labor_eff=0.85,           # كفاءة العمالة: 85%
    region="قطاع الرياض",      # المنطقة
    size="متوسط",             # حجم المشروع
    budget=1000000,           # الميزانية: مليون ريال
    days=180,                 # مدة المشروع: 180 يوم
    risk_desc="تأخيرات محتملة في الحصول على المواد الأولية"
)

print(f"✓ مكونات التأخير:")
for factor, value in delay_analysis['components'].items():
    print(f"  • {factor}: {value:.2f} days")
print(f"\n✓ إجمالي التأخير المتوقع: {delay_analysis['total']:.1f} days")
print(f"✓ العامل الأساسي: {delay_analysis['primary_factor']}")

# ✅ مثال 2: حساب معدل الخطر
print("\n" + "=" * 60)
print("⚠️  مثال 2: حساب معدل الخطر")
print("=" * 60)

risk_percentage = analyzer.calculate_ai_risk_percentage(
    delay=delay_analysis['total'],
    days=180,
    labor_eff=0.85,
    budget=1000000
)

print(f"✓ معدل الخطر: {risk_percentage}%")
if risk_percentage > 75:
    severity = "🔴 Critical"
elif risk_percentage > 60:
    severity = "🟠 High"
elif risk_percentage > 40:
    severity = "🟡 Medium"
else:
    severity = "🟢 Low"
print(f"✓ مستوى الخطورة: {severity}")

# ✅ مثال 3: حساب تجاوز التكاليف
print("\n" + "=" * 60)
print("💰 مثال 3: حساب تجاوز التكاليف")
print("=" * 60)

cost_overrun = analyzer.calculate_advanced_cost_overrun(
    delay=delay_analysis['total'],
    days=180,
    budget=1000000,
    labor_eff=0.85
)

print(f"✓ نسبة تجاوز التكاليف: {cost_overrun}%")
print(f"✓ المبلغ المتوقع للتجاوز: {(1000000 * cost_overrun / 100):,.0f} SAR")

# ✅ مثال 4: حساب معدل التضخم
print("\n" + "=" * 60)
print("📈 مثال 4: حساب معدل التضخم")
print("=" * 60)

inflation = analyzer.calculate_advanced_inflation(
    region="قطاع الرياض",
    days=180,
    budget=1000000
)

print(f"✓ معدل التضخم المتوقع: {inflation}%")
print(f"✓ المبلغ التضخمي على الميزانية: {(1000000 * inflation / 100):,.0f} SAR")

# ✅ مثال 5: حساب البصمة الكربونية
print("\n" + "=" * 60)
print("🌍 مثال 5: حساب البصمة الكربونية")
print("=" * 60)

carbon = analyzer.calculate_advanced_carbon(
    region="قطاع الرياض",
    size="متوسط",
    days=180,
    labor_eff=0.85
)

print(f"✓ البصمة الكربونية: {carbon} طن CO₂")
print(f"✓ التصنيف البيئي: {'🟢 منخفض' if carbon < 150 else '🟡 متوسط' if carbon < 300 else '🔴 عالي'}")

# ✅ مثال 6: الاستنتاجات والتوصيات الذكية
print("\n" + "=" * 60)
print("🤖 مثال 6: الاستنتاجات الذكية")
print("=" * 60)

# حساب مؤشر الامتثال (compliance) - مثال بسيط
compliance_score = max(0, 100 - (risk_percentage * 1.2))

insights = analyzer.generate_ai_insights(
    delay_analysis=delay_analysis,
    cost_overrun=cost_overrun,
    risk_level=risk_percentage,
    compliance=compliance_score
)

print(f"✓ مستوى الخطورة: {insights['severity']}")
print(f"✓ مستوى الثقة: {insights['confidence']*100:.0f}%")
print(f"\n✓ التوصية الأساسية:")
print(f"   {insights['primary_recommendation']}")
print(f"\n✓ التوصيات الإضافية:")
for i, rec in enumerate(insights['secondary_recommendations'], 1):
    print(f"   {i}. {rec}")

# ✅ مثال 7: سيناريوهات الجدول الزمني
print("\n" + "=" * 60)
print("📅 مثال 7: سيناريوهات الجدول الزمني")
print("=" * 60)

scenarios = analyzer.predict_timeline_scenarios(
    current_delay=delay_analysis['total'],
    days=180
)

print(f"✓ أفضل حالة: {scenarios['best_case']} أيام تأخير (تحسن 40%)")
print(f"✓ الحالة الواقعية: {scenarios['realistic_case']} أيام تأخير")
print(f"✓ أسوأ حالة: {scenarios['worst_case']} أيام تأخير (تدهور 50%)")
print(f"✓ فترة الثقة: ± {scenarios['confidence_interval']} أيام")

print("\n" + "=" * 60)
print("✅ انتهى العرض التوضيحي")
print("=" * 60)

# ✅ مثال 8: مقارنة سيناريوهات مختلفة
print("\n" + "=" * 60)
print("🔄 مثال 8: مقارنة الحالات المختلفة")
print("=" * 60)

cases = [
    ("حالة 1: كفاءة عالية (95%)", 0.95, "قطاع الرياض", "صغير", 500000),
    ("حالة 2: كفاءة متوسطة (85%)", 0.85, "نيوم", "متوسط", 1000000),
    ("حالة 3: كفاءة منخفضة (70%)", 0.70, "جدة", "كبير", 2000000),
]

for case_name, labor, region, size, budget in cases:
    analysis = analyzer.calculate_advanced_delay(
        labor_eff=labor,
        region=region,
        size=size,
        budget=budget,
        days=180,
        risk_desc="مخاطر عادية"
    )
    risk = analyzer.calculate_ai_risk_percentage(
        delay=analysis['total'],
        days=180,
        labor_eff=labor,
        budget=budget
    )
    print(f"\n📌 {case_name}")
    print(f"   تأخير: {analysis['total']:.1f} يوم")
    print(f"   خطورة: {risk}%")
    print(f"   العامل الأساسي: {analysis['primary_factor']}")
