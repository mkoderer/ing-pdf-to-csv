from subprocess import getstatusoutput
import re
import sys

# CVS values
print ("Buchung;Valuta;Auftraggeber/Empfänger;Buchungstext;Verwendungszweck;Saldo;Währung;Betrag;Währung")

for fn in sys.argv[1:]:
    # we use iconv to ignore the encoding issues
    # TODO: better to use subprocess for this
    ret, output = getstatusoutput("pdftotext %s -layout -nopgbrk -| iconv --to-code utf-8//IGNORE" % fn)
    if ret != 0:
        print ("Error while reading file %s:" % fn)
        raise Exception(output)

    first_line_date_value = r'.*(\d\d\.\d\d\.\d\d\d\d) +(.*) +(.*,\d\d)'
    sec_line_date = r'.*(\d\d\.\d\d\.\d\d\d\d) +(.*)'
    first_line = None
    for line in output.split('\n'):
        m = re.match(first_line_date_value, line)
        if m and first_line is None:
            first_line = m
        else:
            m = re.match(sec_line_date, line)
            if m and first_line != "":
                date = first_line.group(1)
                valuta = m.group(1)
                type_emp = first_line.group(2).rstrip()
                type_emp = type_emp.split(" ", 1)
                trans_type = type_emp[0]
                try:
                    empf = type_emp[1]
                except:
                    empf = trans_type
                text = m.group(2)
                value = first_line.group(3)
                csv_line = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (date, valuta, empf, trans_type, text, value ,"EUR", value, "EUR")
                print (csv_line)
                first_line = None
            else:
                first_line = None
