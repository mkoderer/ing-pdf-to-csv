from subprocess import getstatusoutput
import re
import sys

# CVS values
print ("Buchung;Valuta;Auftraggeber/Empfänger;Buchungstext;Verwendungszweck;Betrag;Währung;Mandat;Referenz")

for fn in sys.argv[1:]:
    # we use iconv to ignore the encoding issues
    # TODO: better to use subprocess for this
    ret, output = getstatusoutput("pdftotext %s -layout -nopgbrk -| iconv --to-code utf-8//IGNORE" % fn)
    if ret != 0:
        print ("Error while reading file %s:" % fn)
        raise Exception(output)

    first_line_date_value = r'^\s+(\d{2}\.\d{2}\.\d{4})\s+(.*)\s+(\-{0,1}[\.\d]{1,},\d{2})$'
    sec_line_date = r'^\s+(\d{2}\.\d{2}\.\d{4})\s*(.*)$'
    sec_line_desc = r'^\s+(.*)$'
    mandat_line = r'^Mandat:\s(.*)$'
    referenz_line = r'^Referenz:\s(.*)$'
    end_of_line = r'^\s*$'

    i = -1
    parsed_lines=[]
    end = True

    for line in output.split('\n'):
        if re.match(end_of_line, line):
            end = True
            continue

        m = re.match(first_line_date_value, line)
        if m:
            end = False
            i += 1

            type_emp = m.group(2).rstrip()
            type_emp = type_emp.split(" ", 1)
            trans_type = type_emp[0]
            try:
                empf = type_emp[1]
            except:
                empf = trans_type

            parsed_lines.insert(i, {
                "date": m.group(1),
                "empf": empf,
                "trans_type": trans_type,
                "value": m.group(3),
                "valuta": None,
                "text": None,
                "mandat": '',
                "referenz": ''
            })
        elif i >= 0:
            m = re.match(sec_line_date, line)
            if m and parsed_lines[i]:
                parsed_lines[i]["valuta"] = m.group(1)
                parsed_lines[i]["text"] = m.group(2) if m.group(2) is not None else ''
            elif not end:
                m = re.match(sec_line_desc, line)
                if m and parsed_lines[i]:
                    ma = re.match(mandat_line, m.group(1))
                    mr = re.match(referenz_line, m.group(1))
                    if ma:
                        parsed_lines[i]["mandat"] = ma.group(1)
                    elif mr:
                        parsed_lines[i]["referenz"] = mr.group(1)
                    else:
                        parsed_lines[i]["text"] += ", " + m.group(1)

    # finally print the result as CSV
    for line in parsed_lines:
        csv_line = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
                line["date"], line["valuta"],
                line["empf"], line["trans_type"],
                line["text"], line["value"], "EUR",
                line["mandat"], line["referenz"]
            )

        print (csv_line)
