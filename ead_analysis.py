import os,glob,sys,re
from lxml import etree as ET
import datetime
import csv

#Script generates CSV with some statistical info about EADs. Might use in visualization of some kind...

folder = raw_input('Input directory of XMLs: ')
output_file = raw_input('Output_file_name: ')

os.chdir(folder)

writer = csv.writer(open(output_file, 'wb'))

writer.writerow(["eadid", "aleph_id", "title", "extent_info", "series_component_count", "subseries_component_count", "file_component_count", "item_component_count", "total_component_count", "number_of_elements", "chars_in_file", "scopecontent_words", "dsc_scopecontent_words", "bioghist_words", "control_access_count"])


for file in sorted(glob.glob("*.xml")):

	doc = ET.parse(file)
	root = doc.getroot()

	namespace = "{urn:isbn:1-931666-22-9}"
	eadid = root.find(".//{0}eadid".format(namespace)).text
	print eadid
	try:
		aleph_id = root.find(".//{0}num[@type='aleph']".format(namespace)).text
	except:
		aleph_id = "NULL"

	#url = eadid.get('url')
	#date = os.path.getmtime(files)
	#lastmod = datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d')

	title = root.find(".//{0}archdesc/{0}did/{0}unittitle".format(namespace)).text.encode("utf-8")
	title = title.replace('\n','').strip()
	extent_info = root.find(".//{0}archdesc/{0}did/{0}physdesc/{0}extent".format(namespace)).text.encode("utf-8")
	extent_info = extent_info.replace('\n','').strip()


	series_component_count = 0
	subseries_component_count = 0
	file_component_count = 0
	item_component_count = 0
	total_component_count = 0

	#for c01 to c09.
	for i in range(1,10):
		int = i
		for component in root.iter("{0}c0{1}".format(namespace, int)):

			#print component.tag + component.attrib['level']
			if component.attrib["level".format(namespace)] == "series":
				series_component_count = series_component_count + 1
			if component.attrib["level".format(namespace)] == "subseries":
				subseries_component_count = subseries_component_count + 1
			if component.attrib["level".format(namespace)] == "file":
				file_component_count = file_component_count + 1
			if component.attrib["level".format(namespace)] == "item":
				item_component_count = item_component_count + 1
			total_component_count = total_component_count + 1

	#for c10-c12 ... god help me if there are any of these
	for i in range(10,13):
		int = i
		for component in root.iter("{0}c{1}".format(namespace, int)):

			#print component.tag + component.attrib['level']
			if component.attrib["level".format(namespace)] == "series":
				series_component_count = series_component_count + 1
			if component.attrib["level".format(namespace)] == "subseries":
				subseries_component_count = subseries_component_count + 1
			if component.attrib["level".format(namespace)] == "file":
				file_component_count = file_component_count + 1
			if component.attrib["level".format(namespace)] == "item":
				item_component_count = item_component_count + 1
			total_component_count = total_component_count + 1

	num_of_elements = len(root.xpath(".//*"))

	utf8_text=open(file).read()
	unicode_data = utf8_text.decode('utf8')
	characters_in_file = len(unicode_data)

	#collection-level scopecontent charcater count
	#CONFIRM THAT THIS IS GETTING ALL <P>S AND NOT JUST THE FIRST ONE
	collection_level_scopecontent_words = 0
	try:
		for scopecontent in root.findall(".//{0}archdesc/{0}scopecontent/{0}p".format(namespace)):
			collection_level_scopecontent_words = collection_level_scopecontent_words + len(scopecontent.text.encode('utf8').split())
	except:
		pass

	bioghist_word_count = 0
	try:
		for bioghist in root.findall(".//{0}archdesc/{0}bioghist/{0}p".format(namespace)):
			bioghist_word_count = bioghist_word_count + len(bioghist.text.encode('utf8').split())
	except:
		pass

	dsc_scopecontent_word_count = 0
	try:
		for dsc_scopecontent in root.findall(".//{0}dsc//{0}scopecontent/{0}p".format(namespace)):
			dsc_scopecontent_word_count = dsc_scopecontent_word_count + len(dsc_scopecontent.text.encode('utf8').split())
	except:
		pass


	#Calculate number of subjects
	control_access_count = 0
	for subject_term in root.iter("{0}subject".format(namespace)):
		control_access_count = control_access_count + 1
	for geogname_term in root.iter("{0}geogname".format(namespace)):
		control_access_count = control_access_count + 1
	for genreform_term in root.iter("{0}genreform".format(namespace)):
		control_access_count = control_access_count + 1
	for persname_term in root.iter("{0}persname".format(namespace)):
		control_access_count = control_access_count + 1
	for corpname_term in root.iter("{0}corpname".format(namespace)):
		control_access_count = control_access_count + 1



#date of finding aid publication?

#write out columns
	row = []
	row.append(eadid)
	row.append(aleph_id)
	row.append(title)
	row.append(extent_info)
	row.append(series_component_count)
	row.append(subseries_component_count)
	row.append(file_component_count)
	row.append(item_component_count)
	row.append(total_component_count)
	row.append(num_of_elements)
	row.append(characters_in_file)
	row.append(collection_level_scopecontent_words)
	row.append(dsc_scopecontent_word_count)
	row.append(bioghist_word_count)
	row.append(control_access_count)

	writer.writerow(row)
