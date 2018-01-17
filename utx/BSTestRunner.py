# -*- coding: UTF-8 -*-
"""
Copyright (c) 2004-2007, Wai Yip Tung
Copyright (c) 2016, Eason Han
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import json
import shutil
import time

import os

from . import log, setting
import datetime
import io
import sys
import unittest
from xml.sax import saxutils

__author__ = "Wai Yip Tung && Eason Han"
__version__ = "0.8.4"

result_data = dict()
result_data['testResult'] = []
current_class_name = ""


class Template_mixin:
    STATUS = {
        0: 'Pass',
        1: 'Fail',
        2: 'Error',
        3: 'Skip',
    }

    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<!DOCTYPE html>
<html lang="zh-cn">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css">
    %(stylesheet)s

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="http://cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="http://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:Skip; 3:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;


        if (id.substr(0, 2) === 'ft') {
            if (level === 1 || level === 3) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
        if (id.substr(0, 2) === 'pt') {
            if (level === 3) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
        if (id.substr(0, 2) === 'st') {
            if (level === 2 || level === 3) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}

function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        if (!tr) {
            tid = 's' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            if(document.getElementById('div_'+tid)){
                document.getElementById('div_'+tid).style.display = 'none'
            }            
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
--></script>

<div class="main_container">
    %(heading)s
    
    %(report)s
</div>
</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">

.btn-sg-pass {
  color: #333; 
  background-color: #fff;
  border-color: #ccc;
  font-size: 15px;
}

.btn-sg-fail {
  color: #fff;
  background-color: #d9534f;
  border-color: #ccc;
  font-size: 15px;
}

.main_container{
    width: 1500px;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
}

/* -- css div popup ------------------------------------------------------------------------ */
.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #99CCFF;
    font-family: "Microsoft YaHei","Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 10pt;
    width: 800px;
}

/* -- report ------------------------------------------------------------------------ */

#show_detail_line .label {
    font-size: 85%;
    cursor: pointer;
}

#show_detail_line {
    margin: 2em auto 1em auto;
}

#total_row  { font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }

</style>
"""

    HEADING_TMPL = """<div class='heading head_container'>
<h2>%(title)s</h2>
%(parameters)s
<p class='description'>%(description)s</p>


"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p><strong>%(name)s:</strong> %(value)s</p>
"""
    REPORT_TMPL = """

    <p id='show_detail_line'>
    <span class="label label-primary" onclick="showCase(0)">Summary</span>
    <span class="label label-danger" onclick="showCase(1)">Failed</span>
    <span class="label label-info" onclick="showCase(2)">Skip</span>
    <span class="label label-default" onclick="showCase(3)">All</span>
    </p>
</div>
<div>
<table id='result_table' class="table">
    <thead>
        <tr id='header_row'>
            <th>Test Group/Test case</td>
            <th>Count</td>
            <th>Pass</td>
            <th>Fail</td>
            <th>Error</td>
            <th>Skip</td>
            <th>View</td>
        </tr>
    </thead>
    <tbody>
        %(test_list)s
    </tbody>
    <tfoot>
        <tr id='total_row'>
            <td>Total</td>
            <td>%(count)s</td>
            <td class="text text-success">%(Pass)s</td>
            <td class="text text-danger">%(fail)s</td>
            <td class="text text-warning">%(error)s</td>
            <td class="text text-warning">%(skip)s</td>
            <td>&nbsp;</td>
        </tr>
    </tfoot>
</table>
</div>
"""

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>%(skip)s</td>
    <td><a class="btn btn-xs btn-primary"href="javascript:showClassDetail('%(cid)s',%(count)s)">Detail</a></td>
</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    REPORT_TEST_WITH_OUTPUT_TMPL_PASS = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link btn btn-xs btn-sg-pass" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_WITH_OUTPUT_TMPL_FAIL = r"""
    <tr id='%(tid)s' class='%(Class)s'>
        <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
        <td colspan='5' align='center'>

        <!--css div popup start-->
        <a class="popup_link btn btn-xs btn-sg-fail" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
            %(status)s</a>

        <div id='div_%(tid)s' class="popup_window">
            <div style='text-align: right;cursor:pointer'>
            <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
               [x]</a>
            </div>
            <pre>
            %(script)s
            </pre>
        </div>
        <!--css div popup end-->

        </td>
    </tr>
    """  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(output)s
"""


class _TestResult(unittest.TestResult):
    def __init__(self, verbosity=1):
        super().__init__(verbosity)
        self.outputBuffer = io.StringIO()
        self.raw_stdout = None
        self.raw_stderr = None
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []
        self._case_start_time = 0
        self._case_run_time = 0

    def startTest(self, test):
        self._case_start_time = time.time()
        super().startTest(test)
        self.raw_stdout = sys.stdout
        self.raw_stderr = sys.stderr
        sys.stdout = self.outputBuffer
        sys.stderr = self.outputBuffer

    def complete_output(self):
        self._case_run_time = time.time() - self._case_start_time
        if self.raw_stdout:
            sys.stdout = self.raw_stdout
            sys.stderr = self.raw_stderr

        result = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate()
        return result

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        self.result.append((0, test, output, '', self._case_run_time))

    def addError(self, test, err):
        self.error_count += 1
        super().addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str, self._case_run_time))
        log.error('TestCase Error')
        if setting.show_error_traceback:
            log.error(_exc_str)

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        self.result.append((3, test, "", "", 0.0))

    def addFailure(self, test, err):
        self.failure_count += 1
        super().addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str, self._case_run_time))
        log.error('TestCase Failed')
        if setting.show_error_traceback:
            log.error(_exc_str)


class BSTestRunner(Template_mixin):
    def __init__(self, report_title, report_dir, verbosity=1, description=""):
        self.report_dir = report_dir
        self.verbosity = verbosity
        self.title = report_title
        self.description = description
        self.start_time = datetime.datetime.now()
        self.stop_time = None

    def run(self, test):
        log.info("开始进行测试")
        result = _TestResult(self.verbosity)
        test(result)
        self.stop_time = datetime.datetime.now()
        self.generate_report(result)
        log.info('Time Elapsed: {}'.format(self.stop_time - self.start_time))

        if setting.create_ztest_style_report:
            file = os.path.join(self.report_dir, r"{}-ztest.html".format(self.start_time.strftime("%Y-%m-%d-%H-%M-%S")))
            shutil.copy2(os.path.join(os.path.dirname(__file__), "template.html"), file)
            with open(file, "r+", encoding='utf-8') as f:
                content = f.read().replace(r"${resultData}", json.dumps(result_data, ensure_ascii=False, indent=4))
                f.seek(0)
                f.write(content)

    @staticmethod
    def sort_result(case_results):
        rmap = {}
        classes = []
        for n, t, o, e, run_time in case_results:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e, run_time))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def get_report_attributes(self, result):
        start_time = str(self.start_time)[:19]
        duration = str(self.stop_time - self.start_time)
        status = []
        if result.success_count:
            status.append('<span class="text text-success">Pass <strong>%s</strong></span>' % result.success_count)
        if result.failure_count:
            status.append('<span class="text text-danger">Failure <strong>%s</strong></span>' % result.failure_count)
        if result.error_count:
            status.append('<span class="text text-warning">Error <strong>%s</strong></span>' % result.error_count)
        if result.skip_count:
            status.append('<span class="text text-info">Skip <strong>%s</strong></span>' % result.skip_count)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'

        result_data["testName"] = self.title
        result_data["beginTime"] = start_time
        result_data["totalTime"] = duration
        return [
            ('Start Time', start_time),
            ('Duration', duration),
            ('Status', status),
        ]

    def generate_report(self, result):
        report_attrs = self.get_report_attributes(result)
        generator = 'BSTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        output = self.HTML_TMPL % dict(
            title=self.title,
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report)
        if setting.create_bstest_style_report:
            with open(os.path.join(self.report_dir, "{}-bstest.html".format(self.start_time.strftime("%Y-%m-%d-%H-%M-%S"))),
                      "wb") as f:
                f.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=name,
                value=value,
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            pass_num = fail_num = error_num = skip_num = 0
            for case_state, *_ in cls_results:
                if case_state == 0:
                    pass_num += 1
                elif case_state == 1:
                    fail_num += 1
                elif case_state == 2:
                    error_num += 1
                else:
                    skip_num += 1

            name = "{}.{}".format(cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name
            global current_class_name
            current_class_name = name

            row = self.REPORT_CLASS_TMPL % dict(
                style=error_num > 0 and 'text text-warning' or fail_num > 0 and 'text text-danger' or 'text text-success',
                desc=desc,
                count=pass_num + fail_num + error_num + skip_num,
                Pass=pass_num,
                fail=fail_num,
                error=error_num,
                skip=skip_num,
                cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (case_state, t, o, e, run_time) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, case_state, t, o, e, run_time)

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            count=str(result.success_count + result.failure_count + result.error_count + result.skip_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            skip=str(result.skip_count),
        )

        result_data["testPass"] = result.success_count
        result_data["testAll"] = result.success_count + result.failure_count + result.error_count + result.skip_count
        result_data["testFail"] = result.failure_count
        result_data["testSkip"] = result.skip_count

        return report

    def _generate_report_test(self, rows, class_id, case_id, n, t, o, e, run_time):
        has_output = bool(o or e)
        if n == 0:
            case_tr_id = "pt{}.{}".format(class_id + 1, case_id + 1)
        elif n == 1:
            case_tr_id = "ft{}.{}".format(class_id + 1, case_id + 1)
        elif n == 2:
            case_tr_id = "ft{}.{}".format(class_id + 1, case_id + 1)
        elif n == 3:
            case_tr_id = "st{}.{}".format(class_id + 1, case_id + 1)
        else:
            case_tr_id = ""
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl_pass = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL_PASS or self.REPORT_TEST_NO_OUTPUT_TMPL
        tmpl_fail = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL_FAIL or self.REPORT_TEST_NO_OUTPUT_TMPL

        ouptut = self.REPORT_TEST_OUTPUT_TMPL % dict(
            output=saxutils.escape(o + e),
        )

        case_data = {}
        global current_class_name
        case_data['className'] = current_class_name
        case_data['methodName'] = name
        case_data['spendTime'] = "{:.2}S".format(run_time)
        case_data['description'] = doc
        case_data['log'] = o + e
        if self.STATUS[n] == "Pass":
            case_data['status'] = "成功"
        if self.STATUS[n] == "Fail":
            case_data['status'] = "失败"
        if self.STATUS[n] == "Error":
            case_data['status'] = "错误"
        if self.STATUS[n] == "Skip":
            case_data['status'] = "跳过"
        result_data['testResult'].append(case_data)

        if self.STATUS[n] == "Pass":
            row = tmpl_pass % dict(
                tid=case_tr_id,
                Class=(n == 0 and 'hiddenRow' or 'text text-success'),
                style=n == 2 and 'text text-warning' or (n == 1 and 'text text-danger' or 'text text-success'),
                desc=desc,
                script=ouptut,
                status=self.STATUS[n],
            )
        else:
            row = tmpl_fail % dict(
                tid=case_tr_id,
                Class=(n == 0 and 'hiddenRow' or 'text text-success'),
                style=n == 2 and 'text text-warning' or (n == 1 and 'text text-danger' or 'text text-success'),
                desc=desc,
                script=ouptut,
                status=self.STATUS[n],
            )

        rows.append(row)
