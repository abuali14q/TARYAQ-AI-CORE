#!/usr/bin/env python3
"""
✅ فحص صحة الكود والملفات
Code Validation Script
"""

import os
import sys

def check_files_exist():
    """التحقق من وجود الملفات المهمة"""
    print("📂 فحص الملفات...")
    required_files = [
        'app.py',
        'ai_analysis.py',
        'example_usage.py',
        'requirements.txt',
        'logo.png'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - مفقود!")
            return False
    return True

def check_python_syntax():
    """التحقق من صيغة Python"""
    print("\n📝 فحص الصيغة البرمجية...")
    
    files = ['app.py', 'ai_analysis.py', 'example_usage.py']
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, file, 'exec')
            print(f"   ✅ {file} - صيغة صحيحة")
        except SyntaxError as e:
            print(f"   ❌ {file} - خطأ: {e}")
            return False
    return True

def check_imports():
    """التحقق من الاستيرادات"""
    print("\n📦 فحص المكتبات...")
    
    try:
        import numpy
        print("   ✅ numpy")
    except ImportError:
        print("   ❌ numpy - غير مثبت")
        return False
    
    try:
        import pandas
        print("   ✅ pandas")
    except ImportError:
        print("   ❌ pandas - غير مثبت")
        return False
    
    try:
        import plotly
        print("   ✅ plotly")
    except ImportError:
        print("   ❌ plotly - غير مثبت")
        return False
    
    try:
        import streamlit
        print("   ✅ streamlit")
    except ImportError:
        print("   ⚠️  streamlit - غير مثبت (اختياري)")
    
    return True

def check_ai_module():
    """التحقق من وحدة AI"""
    print("\n🤖 فحص وحدة AI...")
    
    try:
        from ai_analysis import AIProjectAnalyzer
        analyzer = AIProjectAnalyzer()
        print("   ✅ AIProjectAnalyzer - تم التحميل بنجاح")
        
        # اختبار دالة بسيطة
        delay = analyzer.calculate_advanced_delay(
            labor_eff=0.85,
            region="قطاع الرياض",
            size="متوسط",
            budget=1000000,
            days=180,
            risk_desc="test"
        )
        print(f"   ✅ حساب التأخير: {delay['total']:.1f} أيام")
        
        return True
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        return False

def check_documentation():
    """التحقق من التوثيق"""
    print("\n📚 فحص ملفات التوثيق...")
    
    doc_files = [
        'README_NEW.md',
        'AI_ENHANCEMENTS.md',
        'ENHANCEMENT_SUMMARY.md',
        'COMPLETION.md',
        'START_HERE.md'
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ⚠️  {file} - غير موجود")
    
    return True

def main():
    """فحص شامل"""
    print("=" * 60)
    print("🔍 فحص شامل للمشروع")
    print("=" * 60)
    
    results = []
    
    results.append(("الملفات", check_files_exist()))
    results.append(("الصيغة البرمجية", check_python_syntax()))
    results.append(("المكتبات", check_imports()))
    results.append(("وحدة AI", check_ai_module()))
    results.append(("التوثيق", check_documentation()))
    
    print("\n" + "=" * 60)
    print("📊 ملخص الفحص:")
    print("=" * 60)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("✅ جميع الفحوصات نجحت!")
        print("🚀 النظام جاهز للتشغيل")
        return 0
    else:
        print("❌ بعض الفحوصات فشلت")
        print("⚠️  يرجى التحقق من المتطلبات")
        return 1

if __name__ == "__main__":
    sys.exit(main())
