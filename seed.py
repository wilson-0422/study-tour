from app import create_app, db
from app.models.user import User
from app.models.route import Route
from app.models.registration import Registration
from app.models.insurance import Insurance
from app.models.accommodation import Accommodation
from app.models.achievement import Achievement
from app.models.mentor import Mentor
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", name="系统管理员", email="admin@studytour.cn", role="admin", phone="13800000001")
    admin.set_password("admin123")
    db.session.add(admin)

    teacher = User(username="zhanglaoshi", name="张老师", email="zhang@studytour.cn", role="teacher", phone="13800000002")
    teacher.set_password("123456")
    db.session.add(teacher)

    students_data = [
        ("liming", "李明", "liming@studytour.cn", "13800000011"),
        ("wangfang", "王芳", "wangfang@studytour.cn", "13800000012"),
        ("zhaowei", "赵伟", "zhaowei@studytour.cn", "13800000013"),
        ("liuna", "刘娜", "liuna@studytour.cn", "13800000014"),
        ("chenyang", "陈洋", "chenyang@studytour.cn", "13800000015"),
        ("sunli", "孙丽", "sunli@studytour.cn", "13800000016"),
        ("zhoujie", "周杰", "zhoujie@studytour.cn", "13800000017"),
        ("wumin", "吴敏", "wumin@studytour.cn", "13800000018"),
    ]
    students = []
    for uname, name, email, phone in students_data:
        s = User(username=uname, name=name, email=email, role="student", phone=phone)
        s.set_password("123456")
        db.session.add(s)
        students.append(s)

    db.session.flush()

    mentors_data = [
        ("wangdaoshi", "王导师", "wangds@studytour.cn", "13800000021", "历史文化研究", "北京大学历史学博士，专注青少年研学教育10年"),
        ("lidaoshi", "李导师", "lids@studytour.cn", "13800000022", "自然科学探索", "中科院生态学硕士，自然教育资深讲师"),
        ("zhangdaoshi", "张导师", "zhangds@studytour.cn", "13800000023", "科技创新实践", "清华大学计算机博士，创客教育专家"),
    ]
    mentor_objs = []
    for uname, name, email, phone, specialty, bio in mentors_data:
        u = User(username=uname, name=name, email=email, role="mentor", phone=phone)
        u.set_password("123456")
        db.session.add(u)
        db.session.flush()
        m = Mentor(user_id=u.id, name=name, specialty=specialty, bio=bio)
        db.session.add(m)
        mentor_objs.append(m)

    db.session.flush()

    routes_data = [
        ("古都西安文化探秘之旅", "西安", "深入十三朝古都，探访兵马俑、大雁塔、城墙等历史遗迹，感受千年文化底蕴", 5, 2980, 40, date(2024, 7, 10), date(2024, 7, 14), "published", teacher.id),
        ("张家界自然生态研学行", "张家界", "走进世界自然遗产，探索地质奇观，学习生态保护知识，体验土家族文化", 4, 2580, 35, date(2024, 7, 20), date(2024, 7, 23), "published", teacher.id),
        ("深圳科技创新体验营", "深圳", "参观华为、腾讯等科技企业，体验前沿科技，激发创新思维", 3, 3280, 30, date(2024, 8, 5), date(2024, 8, 7), "published", admin.id),
        ("敦煌丝路文化研学之旅", "敦煌", "追寻丝绸之路足迹，探访莫高窟艺术宝库，体验大漠风光", 6, 3580, 25, date(2024, 8, 15), date(2024, 8, 20), "draft", teacher.id),
        ("杭州互联网创业研学营", "杭州", "走进阿里巴巴等互联网企业，了解电商生态，学习创业思维", 4, 2880, 30, date(2024, 9, 1), date(2024, 9, 4), "draft", admin.id),
    ]
    route_objs = []
    for name, dest, desc, dur, price, max_s, start, end, status, created_by in routes_data:
        r = Route(name=name, destination=dest, description=desc, duration=dur,
                  price=price, max_students=max_s, start_date=start, end_date=end,
                  status=status, created_by=created_by)
        db.session.add(r)
        route_objs.append(r)

    db.session.flush()

    reg_data = [
        (students[0].id, route_objs[0].id, "approved", "对历史文化非常感兴趣"),
        (students[1].id, route_objs[0].id, "approved", ""),
        (students[2].id, route_objs[1].id, "approved", "喜欢自然探索"),
        (students[3].id, route_objs[1].id, "pending", ""),
        (students[4].id, route_objs[2].id, "approved", "对科技很感兴趣"),
        (students[5].id, route_objs[2].id, "pending", "希望了解互联网行业"),
        (students[6].id, route_objs[0].id, "rejected", "时间冲突"),
        (students[7].id, route_objs[1].id, "approved", ""),
    ]
    reg_objs = []
    for sid, rid, status, notes in reg_data:
        r = Registration(student_id=sid, route_id=rid, status=status, notes=notes)
        db.session.add(r)
        reg_objs.append(r)

    db.session.flush()

    ins_data = [
        (reg_objs[0].id, "中国人保", "PICC20240710001", 500000, date(2024, 7, 10), date(2024, 7, 14), 35),
        (reg_objs[1].id, "中国人保", "PICC20240710002", 500000, date(2024, 7, 10), date(2024, 7, 14), 35),
        (reg_objs[2].id, "中国平安", "PING20240720001", 500000, date(2024, 7, 20), date(2024, 7, 23), 30),
        (reg_objs[4].id, "太平洋保险", "CPIC20240805001", 500000, date(2024, 8, 5), date(2024, 8, 7), 28),
        (reg_objs[7].id, "中国平安", "PING20240720002", 500000, date(2024, 7, 20), date(2024, 7, 23), 30),
    ]
    for reg_id, provider, policy, coverage, start, end, premium in ins_data:
        i = Insurance(registration_id=reg_id, provider=provider, policy_number=policy,
                      coverage_amount=coverage, start_date=start, end_date=end, premium=premium)
        db.session.add(i)

    acc_data = [
        (route_objs[0].id, "西安钟楼饭店", "西安市碑林区南大街110号", date(2024, 7, 10), date(2024, 7, 14), "标准双人间", True, 280),
        (route_objs[1].id, "张家界武陵源酒店", "张家界市武陵源区军地坪", date(2024, 7, 20), date(2024, 7, 23), "标准双人间", True, 320),
        (route_objs[2].id, "深圳南山科技园酒店", "深圳市南山区科技园路88号", date(2024, 8, 5), date(2024, 8, 7), "标准单人间", False, 380),
        (route_objs[3].id, "敦煌丝路饭店", "敦煌市阳关东路1号", date(2024, 8, 15), date(2024, 8, 20), "标准双人间", True, 260),
    ]
    for rid, hotel, addr, ci, co, room, meals, cost in acc_data:
        a = Accommodation(route_id=rid, hotel_name=hotel, address=addr,
                          check_in=ci, check_out=co, room_type=room,
                          meals_included=meals, cost_per_person=cost)
        db.session.add(a)

    ach_data = [
        (students[0].id, route_objs[0].id, "西安文化探秘研学报告", "通过本次西安研学，我深入了解了秦始皇兵马俑的历史背景和制作工艺，参观了大雁塔的佛教文化遗存，登上了古城墙感受千年历史。这次研学让我对中国古代文明有了更加直观的认识，也增强了我的文化自信。", 92, "报告内容详实，感悟深刻，体现了良好的研学态度"),
        (students[1].id, route_objs[0].id, "古都西安之旅心得体会", "西安之行让我印象深刻，特别是兵马俑的壮观让我震撼。通过实地参观，我对课本上的历史知识有了更深的理解。", 85, "心得真实，但可以增加更多深度思考"),
        (students[2].id, route_objs[1].id, "张家界生态保护调研报告", "本次研学我重点关注了张家界的地质构造和生态保护措施，了解了石英砂岩峰林地貌的形成过程，也学习了当地在生态保护方面的努力。", 88, "调研角度独特，数据详实，建议补充保护建议"),
        (students[4].id, route_objs[2].id, "深圳科技创新体验总结", "参观华为和腾讯让我对中国科技企业有了更深入的了解，感受到了科技创新的力量。我对人工智能和云计算产生了浓厚兴趣。", None, None),
    ]
    for sid, rid, title, content, score, feedback in ach_data:
        a = Achievement(student_id=sid, route_id=rid, title=title, content=content,
                        score=score, feedback=feedback)
        db.session.add(a)

    mentor_objs[0].rating = 8.5
    mentor_objs[0].total_evaluations = 4
    mentor_objs[1].rating = 9.0
    mentor_objs[1].total_evaluations = 3
    mentor_objs[2].rating = 7.8
    mentor_objs[2].total_evaluations = 5

    db.session.commit()

    print("种子数据初始化完成！")
    print("管理员账号: admin / admin123")
    print("教师账号: zhanglaoshi / 123456")
    print("学生账号: liming / 123456")
    print("导师账号: wangdaoshi / 123456")
