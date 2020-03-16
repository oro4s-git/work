tall = float(input("身長を入力してください（cm）:\n"))
wait = float(input("体重を入力してください（kg）：\n"))

bmi = wait/((tall/100)**2)
best = ((tall/100)**2)*22

if bmi < 18.5:
    hantei = "やせ型"
elif bmi < 25:
    hantei = "普通体重"
elif bmi < 30:
    hantei = "肥満（1度）"
elif bmi < 35:
    hantei = "肥満（2度）"
elif bmi < 40:
    hantei = "肥満（3度）"
else:
    hantei = "肥満（4度）"

print("\nBMI値は {0:.1f} ".format(bmi) + "【" + hantei + "】"  + "です")
print("ベスト体重は {0:.1f} kgです".format(best))
