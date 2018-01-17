utx
---

> 支持Python3.5及以上版本

utx扩展了Python unittest框架的功能，起因是需要控制测试用例的执行顺序，而unittest的默认执行顺序是按照用例函数的名称进行排序，所以想要做一个可以无缝接入unittest的扩展功能库。


安装utx
-----
```python
python setup.py install
```

更新utx
-----

```python
pip uninstall utx   # 需要先卸载旧的utx
python setup.py install
```



功能列表
----

- 用例排序，只需要导入utx库，用例的执行顺序就会和编写顺序一致

- 用例自定义标签，在 case_tag.py 里边添加标签，可以对测试用例指定多标签

```python
@unique
class Tag(Enum):
    SMOKE = 1  # 冒烟测试标记，可以重命名，但是不要删除
    FULL = 1000  # 完整测试标记，可以重命名，但是不要删除

    # 以下开始为扩展标签，自行调整
    SP = 2
```

```python
class TestLegion(unittest.TestCase):

    @tag(Tag.SMOKE)
    def test_create_legion(self):
        pass
```

- 运行指定标签的测试用例

```python
from utx import *

if __name__ == '__main__':
    setting.run_case = {Tag.SMOKE}  # 只运行SMOKE冒烟用例
    # setting.run_case = {Tag.FULL}  # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行标记为SMOKE和SP的用例

    runner = TestRunner()
    runner.add_case_dir(r"testcase")
    runner.run_test(report_title='接口自动化测试报告')
```

- 数据驱动
```python
class TestLegion(unittest.TestCase):

    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)
        
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        """ 领取祈福宝箱

        :return:
        """
        print(box_id)
```

- 检测用例是否编写了用例描述
```python
2017-11-13 12:00:19,334 WARNING legion.test_legion.test_bless没有用例描述
```

- 执行测试时，显示测试进度
```python
2017-11-13 12:00:19,336 INFO 开始进行测试
2017-11-13 12:00:19,436 INFO Start to test legion.test_legion.test_create_legion (1/5)
2017-11-13 12:00:19,536 INFO Start to test legion.test_legion.test_receive_bless_box (2/5)
2017-11-13 12:00:19,637 INFO Start to test legion.test_legion.test_receive_bless_box (3/5)
2017-11-13 12:00:19,737 INFO Start to test legion.test_legion.test_receive_bless_box (4/5)
2017-11-13 12:00:19,837 INFO Start to test legion.test_legion.test_quit_legion (5/5)
```

- setting类提供多个设置选项进行配置
```python
class setting:

    # 只运行的用例类型
    run_case = {Tag.SMOKE}

    # 开启用例排序
    sort_case = True

    # 每个用例的执行间隔，单位是秒
    execute_interval = 0.1

    # 开启检测用例描述
    check_case_doc = True

    # 显示完整用例名字（函数名字+参数信息）
    full_case_name = False

    # 测试报告显示的用例名字最大程度
    max_case_name_len = 80

    # 执行用例的时候，显示报错信息
    show_error_traceback = True

    # 生成ztest风格的报告
    create_ztest_style_report = True

    # 生成bstest风格的报告
    create_bstest_style_report = True
```


- 集成 [ztest](https://github.com/zhangfei19841004/ztest) 和 [BSTestRunner](https://github.com/easonhan007/HTMLTestRunner) 自动生成两份测试报告，感谢两位作者的测试报告模版~

> ztest风格

![ztest风格](https://github.com/jianbing/utx/raw/master/img/ztest.png)

> bstest风格

![bstest风格](https://github.com/jianbing/utx/raw/master/img/bstest.png)

- 无缝接入unittest项目，导入utx包即可开始使用扩展功能，无需修改之前的代码

---

demo目录下，有几个例子：

- ```run.py```  使用utx的完整功能

- ```just_use_report.py``` 单独使用测试报告组件，不需要utx的其他扩展功能

- ```stop_patch_example.py``` 如果项目使用utx，在调试单个用例的时候，需要先调用utx.stop_patch()，暂停utx对unittest模块的注入