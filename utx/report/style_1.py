#! /usr/bin/env python
# -*- coding: UTF-8 -*-

html_head = r"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{report_name}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>

    <style type="text/css" media="screen">
        pre {{
            white-space: pre-wrap;
            white-space: -moz-pre-wrap;
            white-space: -pre-wrap;
            white-space: -o-pre-wrap;
            word-wrap: break-word;
            text-align: left;
        }}
    
        body {{
            font-family: Microsoft YaHei, Tahoma, arial, helvetica, sans-serif;
            padding: 20px;
            font-size: 80%;
        }}

        table {{
            font-size: 100%;
        }}

        /* -- heading ---------------------------------------------------------------------- */
        .heading {{
            margin-top: 0ex;
            margin-bottom: 1ex;
        }}

        .heading .description {{
            margin-top: 4ex;
            margin-bottom: 6ex;
        }}

        /* -- report ------------------------------------------------------------------------ */
        #total_row {{
            font-weight: bold;
        }}

        .passCase {{
            color: #5cb85c;
        }}

        .failCase {{
            color: #f0ad4e;
            font-weight: bold;
        }}

        .errorCase {{        
            color: #d9534f;
            font-weight: bold;
        }}

        .hiddenRow {{
            display: none;
        }}

        .testcase {{
            margin-left: 2em;
        }}
    </style>

</head>
<script language="javascript" type="text/javascript">
    output_list = Array();


    function showCase(level) {{
        trs = document.getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {{
            tr = trs[i];
            id = tr.id;
            if (id.substr(0, 2) == 'pt') {{
                if (level == 1 || level == 4) {{
                    tr.className = '';
                }}
                else {{
                    tr.className = 'hiddenRow';                    
                }}
            }}
            if (id.substr(0, 2) == 'ft') {{
                if (level == 2 || level == 4) {{
                    tr.className = '';
                }}
                else {{
                    tr.className = 'hiddenRow';
                }}
            }}
            
            if (id.substr(0, 2) == 'et') {{
                if (level == 3 || level == 4) {{
                    tr.className = '';
                }}
                else {{
                    tr.className = 'hiddenRow';
                }}
            }}
        }}

        detail_class = document.getElementsByClassName('detail');
        //console.log(detail_class.length)
        if (level == 3) {{
            for (var i = 0; i < detail_class.length; i++) {{
                detail_class[i].innerHTML = "收起"
            }}
        }}
        else {{
            for (var i = 0; i < detail_class.length; i++) {{
                detail_class[i].innerHTML = "详细"
            }}
        }}
    }}

    function showClassDetail(cid, count) {{
        var id_list = Array(count);
        var toHide = 1;
        for (var i = 0; i < count; i++) {{
            tid0 = 't' + cid.substr(1) + '_' + (i + 1);
            console.log(tid0);
            tid = 'f' + tid0;
            tr = document.getElementById(tid);
            if (!tr) {{
                tid = 'p' + tid0;
                tr = document.getElementById(tid);
            }}
            if (!tr) {{
                tid = 'e' + tid0;
                tr = document.getElementById(tid);
            }}
            id_list[i] = tid;
            if (tr.className) {{
                toHide = 0;
            }}
        }}
        for (var i = 0; i < count; i++) {{
            tid = id_list[i];
            if (toHide) {{
                document.getElementById(tid).className = 'hiddenRow';
                document.getElementById(cid).innerText = "详细"
            }}
            else {{
                document.getElementById(tid).className = '';
                document.getElementById(cid).innerText = "收起"
            }}
        }}
    }}

    function html_escape(s) {{
        s = s.replace(/&/g, '&amp;');
        s = s.replace(/</g, '&lt;');
        s = s.replace(/>/g, '&gt;');
        return s;
    }}
</script>
"""

html_body = """

<body>

<div class='heading'>
    <h1 style="font-family: Microsoft YaHei">{report_name}</h1>
    <p class='attribute'><strong>开始时间 : </strong> {begin_time}</p>
    <p class='attribute'><strong>合计耗时 : </strong> {total_time}</p>
    <p class='attribute'><strong>测试结果 : </strong> 共 {test_all}，通过 {test_pass}，失败 {test_fail}，错误 {test_error}，跳过 {test_skip}，通过率= {test_pass_per}</p>

    <p class='description'></p>
</div>


<p id='show_detail_line'>
    <a class="btn btn-primary" href='javascript:showCase(0)'>概要{{ {test_pass_per} }}</a>
    <a class="btn btn-success" href='javascript:showCase(1)'>通过{{ {test_pass} }}</a>
    <a class="btn btn-warning" href='javascript:showCase(2)'>失败{{ {test_fail} }}</a>
    <a class="btn btn-danger" href='javascript:showCase(3)'>错误{{ {test_error} }}</a>
    <a class="btn btn-info" href='javascript:showCase(4)'>所有{{ {test_all} }}</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
    <colgroup>
        <col align='left'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
    </colgroup>
    <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
        <td>用例集/测试用例</td>
        <td>总计</td>
        <td>通过</td>
        <td>失败</td>
        <td>错误</td>
        <td>跳过</td>
        <td>详细</td>
    </tr>

 
    {case_info}

    <tr id='total_row' class="text-center active">
        <td>总计</td>
        <td>{test_all}</td>
        <td>{test_pass}</td>
        <td>{test_fail}</td>
        <td>{test_error}</td>
        <td>{test_skip}</td>
        <td>通过率：{test_pass_per}</td>
    </tr>
</table>

<div id='ending'>&nbsp;</div>
<div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style="font-size:30px;" aria-hidden="true">
    </span></a></div>


</body>
</html>
"""

html_case_group = """
<tr class="failClass warning">
        <td>{group_name}</td>
        <td class="text-center">{test_all}</td>
        <td class="text-center">{test_pass}</td>
        <td class="text-center">{test_fail}</td>
        <td class="text-center">{test_error}</td>
        <td class="text-center">{test_skip}</td>
        <td class="text-center"><a href="javascript:showClassDetail('c{group_index}',{test_all})" class="detail" id="c{group_index}">详细</a></td>
    </tr>
"""

html_case_skip = """
<tr id="pt{case_id}" class="">
        <td class="passCase">
            <div class="testcase">{method_name}</div>
        </td>
        <td colspan="6" align="center">
        <span class="label label-info success">跳过</span>
        </td>
    </tr>
"""

html_case_pass_no_log = """
<tr id="pt{case_id}" class="">
        <td class="passCase">
            <div class="testcase">{method_name}</div>
        </td>
        <td colspan="6" align="center">
        <span class="label label-success success">通过</span>
        </td>
    </tr>
"""

html_case_pass_with_log = """
<tr id="pt{case_id}" class="">
        <td class="passCase">
            <div class="testcase">{method_name}</div>
        </td>
        <td colspan="6" align="center">
       
        <button id='btn_pt{case_id}' type="button"  class="btn btn-success btn-xs collapsed" data-toggle="collapse" data-target='#div_pt{case_id}'>通过</button>
        <div id='div_pt{case_id}' class="collapse">
                <pre>{case_log}</pre>
            </div>
        </td>
    </tr>
"""

html_case_fail = """
<tr id="ft{case_id}" class="">
        <td class="failCase">
            <div class="testcase">{method_name}</div>
        </td>
        <td colspan="6" align="center">
            <!--默认收起错误信息
            <button id='btn_ft1_2' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_ft1_2'>失败</button>
            <div id='div_ft1_2' class="collapse">  -->

            <!-- 默认展开错误信息 -->
            <button id="btn_ft{case_id}" type="button" class="btn btn-warning btn-xs" data-toggle="collapse" data-target="#div_ft{case_id}">失败</button>
            <div id="div_ft{case_id}" class="collapse in">
                <pre>{case_log}</pre>
            </div>
        </td>
    </tr>
"""

html_case_error = """
<tr id="et{case_id}" class="">
    <td class="errorCase"><div class="testcase">{method_name}</div></td>
    <td colspan="6" align="center">
    <!--默认收起错误信息
    <button id='btn_et1_5' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_et1_5'>错误</button>
    <div id='div_et1_5' class="collapse">  -->

    <!-- 默认展开错误信息 -->
    <button id="btn_et{case_id}" type="button" class="btn btn-danger btn-xs" data-toggle="collapse" data-target="#div_et{case_id}">错误</button>
    <div id="div_et{case_id}" class="collapse in">
        <pre>{case_log}</pre>
    </div>
    </td>
</tr>
"""


def build_report(file_path, data):
    html = html_head.format(report_name=data['reportName'])

    case_info = ""
    from collections import defaultdict
    filter_case = defaultdict(list)
    for i in data['testResult']:
        filter_case[i["className"]].append(i)

    for group_index, group in enumerate(filter_case.keys(), 1):
        pass_num = len([i for i in filter_case[group] if i['status'] == '成功'])
        fail_num = len([i for i in filter_case[group] if i['status'] == '失败'])
        error_num = len([i for i in filter_case[group] if i['status'] == '错误'])
        skip_num = len([i for i in filter_case[group] if i['status'] == '跳过'])
        case_info += html_case_group.format(group_name=group,
                                            group_index=group_index,
                                            test_all=pass_num + fail_num + error_num + skip_num,
                                            test_pass=pass_num,
                                            test_fail=fail_num,
                                            test_error=error_num,
                                            test_skip=skip_num
                                            )
        cases = filter_case[group]
        for case_index, case in enumerate(cases, 1):
            if case['status'] == '成功':
                if case['log']:
                    case_info += html_case_pass_with_log.format(case_id="{}_{}".format(group_index, case_index),
                                                                method_name="{}（{}）".format(case['methodName'],
                                                                                            case['description']),
                                                                case_log=case['log'])
                else:
                    case_info += html_case_pass_no_log.format(case_id="{}_{}".format(group_index, case_index),
                                                              method_name="{}（{}）".format(case['methodName'],
                                                                                          case['description']),
                                                              )
            elif case['status'] == '失败':
                case_info += html_case_fail.format(case_id="{}_{}".format(group_index, case_index),
                                                   method_name="{}（{}）".format(case['methodName'],
                                                                               case['description']),
                                                   case_log=case['log'])
            elif case['status'] == '错误':
                case_info += html_case_error.format(case_id="{}_{}".format(group_index, case_index),
                                                    method_name="{}（{}）".format(case['methodName'],
                                                                                case['description']),
                                                    case_log=case['log'])
            elif case['status'] == '跳过':
                case_info += html_case_skip.format(case_id="{}_{}".format(group_index, case_index),
                                                   method_name="{}（{}）".format(case['methodName'],
                                                                               case['description']),
                                                   )

    html += html_body.format(begin_time=data['beginTime'],
                             total_time=data['totalTime'],
                             test_all=data['testAll'],
                             test_pass=data['testPass'],
                             test_fail=data['testFail'],
                             test_skip=data['testSkip'],
                             test_error=data['testError'],
                             test_pass_per="{:.2%}".format(data['testPass'] / data['testAll']),
                             report_name=data['reportName'],
                             case_info=case_info,
                             )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
