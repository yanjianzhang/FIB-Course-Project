import owlready2 as owl

onto = owl.get_ontology("http://localhost:7200/SDM_lab03")


###Parent classes

# Persons
class Person(owl.Thing):
	namespace = onto

# Papers
class Paper(owl.Thing):
	namespace = onto
	
class SubmittedPaper(Paper):
	namespace = onto
	
# Area
class Area(owl.Thing):
	namespace = onto

# Periodical
class Periodical(owl.Thing):
	namespace = onto

# Review 
class Review(owl.Thing):
	namespace = onto

#EditionProceedings

class Conference(owl.Thing):
	namespace = onto

class Journal(owl.Thing):
	namespace = onto	

	
### Subclasses
class Reviewer(Person):
	namespace = onto

class Author(Person):
	namespace = onto

class ManagingStaff(Person):
	namespace = onto

class Chair(ManagingStaff):
	namespace = onto

class Editor(ManagingStaff):
	namespace = onto

class ReviewedPaper(SubmittedPaper):
	namespace = onto
	
class Accepted_Paper(ReviewedPaper):
	namespace = onto

class Unaccepted_Paper(ReviewedPaper):
	namespace = onto

class EditionProceedings(Periodical):
	namespace = onto

class Volume(Periodical):
	namespace = onto

# class Workshop(Conference):
# 	namespace = onto
#
# class Symposium(Conference):
# 	namespace = onto
#
# class ExpertGroup(Conference):
# 	namespace = onto
#
# class RegularConference(Conference):
# 	namespace = onto

### Relationships

class writes(owl.ObjectProperty):
	namespace = onto
	domain = [Author]
	range = [Paper]

class submittedTo(owl.ObjectProperty):
	namespace = onto
	domain = [Paper]
	range = [SubmittedPaper]
	
class makes(owl.ObjectProperty):
	namespace = onto
	domain = [Reviewer]
	range = [Review]

class reviews(owl.ObjectProperty):
	namespace = onto
	domain = [Reviewer]
	range = [SubmittedPaper]
	
class is_reviewedBy(owl.ObjectProperty):
	namespace = onto
	domain = [SubmittedPaper]
	range = [Reviewer]
	inverse_property = reviews

class assigns(owl.ObjectProperty):
	namespace = onto
	domain = [Chair, Editor]
	range = [Reviewer]

class chairOf(owl.ObjectProperty):
	namespace = onto
	domain = [Chair]
	range = [Conference]

class editorOf(owl.ObjectProperty):
	namespace = onto
	domain = [Editor]
	range = [Journal]

class published(owl.ObjectProperty):
	namespace = onto
	domain = [Accepted_Paper]
	range = [Periodical]

class has_area(owl.ObjectProperty):
	namespace = onto
	domain = [Paper, Journal, Conference]
	range = [Area]

class has_edition(owl.ObjectProperty):
	namespace = onto
	domain = [Conference]
	range = [EditionProceedings]

class is_edition(owl.ObjectProperty):
	namespace = onto
	domain = [EditionProceedings]
	range = [Conference]
	inverse_property = has_edition

class has_volume(owl.ObjectProperty):
	namespace = onto
	domain = [Journal]
	range = [Volume]

class is_volume(owl.ObjectProperty):
	namespace = onto
	domain = [Volume]
	range = [Journal]
	inverse_property = has_volume

class has_review(owl.ObjectProperty):
	namespace = onto
	domain = [ReviewedPaper, Unaccepted_Paper, Accepted_Paper]
	range = [Review]



###Properties

class fullname(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Person, Author, Chair, Editor, Review,
			  Conference, EditionProceedings,
			  Journal, Volume, Area, Periodical ]
	range = [str]

class title(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Paper, Accepted_Paper, Unaccepted_Paper,SubmittedPaper, ReviewedPaper]
	range = [str]

class reviewed(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [SubmittedPaper]
	range = [bool]
	
class accepted(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Paper, SubmittedPaper, ReviewedPaper, Accepted_Paper, Unaccepted_Paper]
	range = [bool]


class periodicaltype(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Periodical]
	range = [str]


class conf_type(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Conference]
	range = [str]

class paper_type(owl.DataProperty, owl.FunctionalProperty):
	namespace = onto
	domain = [Paper, Accepted_Paper, Unaccepted_Paper, SubmittedPaper, ReviewedPaper]
	range = [str]

### Property restrictions

Paper.is_a.append(has_area.some(Area))
Accepted_Paper.equivalent_to.append(SubmittedPaper & accepted.value(True))
Unaccepted_Paper.equivalent_to.append(SubmittedPaper & accepted.value(False))
Volume.equivalent_to.append(Periodical & periodicaltype.value('volume'))
EditionProceedings.equivalent_to.append(Periodical & periodicaltype.value('edition'))


EditionProceedings.is_a.append(is_edition.exactly(1, Conference))
Volume.is_a.append(is_volume.exactly(1, Journal))

Chair.is_a.append(chairOf.some(Conference))
Conference.is_a.append(has_area.some(Area))

Editor.is_a.append(editorOf.some(Journal))
Journal.is_a.append(has_area.some(Area))
 
SubmittedPaper.is_a.append(is_reviewedBy.min(2, Reviewer))
SubmittedPaper.is_a.append(owl.Inverse(submittedTo).exactly(1, Paper))




# Disjoint
owl.AllDisjoint([Accepted_Paper, Unaccepted_Paper])
owl.AllDisjoint([Volume, EditionProceedings])

if __name__ == "__main__":
	dir_ = "../data/tbox.rdf"
	onto.save(file=dir_, format="rdfxml")
	print(f'TBox saved')
