# Data Anonymization: People, Technology and Regulations
Data anonymization, also known as psudeonymization, refers to a family of techniques that make it impossible or impractical to identify a data subject.

## [Privacy Act, Canada](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/02_05_d_15/#heading-0-0-2-1)
The Privacy Act offers protections for personal information, which it defines as any recorded information “about an identifiable individual.”

## [PIPEDA, Canada](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/)
The Personal Information Protection and Electronic Documents Act (PIPEDA), sets the ground rules for how private-sector organizations collect, use, and disclose personal information in the course of for-profit, commercial activities across Canada.

The definition of personal information differs somewhat under PIPEDA or the Privacy Act but generally, it can mean information about your:

- race, national or ethnic origin, religion,
age, marital status,
medical, education or employment history,
- financial information,
- DNA,
- identifying numbers such as your social insurance number, or driver’s licence,
views or opinions about you as an employee.

## [GDPR, EU](https://gdpr-info.eu)

Compliance to General Data Protection Regulation (**GDPR**) has increased the importance of data anonymization because GPPR relaxes it stringent requirements if effective measures are taken to de-identify the people in data. If executed properly, the regulations allow processing, storage and communication of anonymized data.

GDPR defines anonymized data as “information which does not relate to an identified or identifiable natural person or to personal data rendered anonymous in such a manner that the data subject is not or no longer identifiable.”

### **[GDPR, EU Recital 26](https://gdpr-info.eu/recitals/no-26/)** 

1. The principles of data protection should apply to any information concerning an identified or identifiable natural person. 

2. Personal data which have undergone pseudonymisation, which could be attributed to a natural person by the use of additional information should be considered to be information on an identifiable natural person. 

3. To determine whether a natural person is identifiable, account should be taken of all the means reasonably likely to be used, such as singling out, either by the controller or by another person to identify the natural person directly or indirectly. 

4. To ascertain whether means are reasonably likely to be used to identify the natural person, account should be taken of all objective factors, such as the costs of and the amount of time required for identification, taking into consideration the available technology at the time of the processing and technological developments. 

5. **The principles of data protection should therefore not apply to anonymous information, namely information which does not relate to an identified or identifiable natural person or to personal data rendered anonymous in such a manner that the data subject is not or no longer identifiable.**

6. **This Regulation does not therefore concern the processing of such anonymous information, including for statistical or research purposes.**

The data based enterprises, both controllers and processors, who opt to choose data anonymization are not completely safe from stepping across regulatory bounds.

# Concepts

## [Personal Data](https://gdpr-info.eu/issues/personal-data/)
As obvious as it may seem, but GDPR has particularly defined what constitutes *personal data*.

*The data subjects are identifiable if they can be directly or indirectly identified, especially by reference to an identifier such as a name, an identification number, location data, an online identifier or one of several special characteristics, which expresses the physical, physiological, genetic, mental, commercial, cultural or social identity of these natural persons. In practice, these also include all data which are or can be assigned to a person in any kind of way. For example, the telephone, credit card or personnel number of a person, account data, number plate, appearance, customer number or address are all personal data.*

## Anonymization

## [Pseudonymisation](https://gdpr-info.eu/recitals/no-28/)

Pseudonymisation is the process and techniques of de-identifying personal data by substituting it with psuedo information that allows analysis and processing but a natural person can not be identified with that information. It is not as strict as anonymization. Pseudonymizing creates a new attribute that link personal identifiers with psuedonymized data to enable de-anonymization later. The links then become a proxy for real information and get protected by the data controllers while transformed data can be *legaly* stored, processed and transfered.

GDPR recital 28 notes as following:

*The application of pseudonymisation to personal data can reduce the risks to the data subjects concerned and help controllers and processors to meet their data-protection obligations. 
2. The explicit introduction of ‘pseudonymisation’ in this Regulation is not intended to preclude any other measures of data protection.*


# Techniques
In consideration of compliance to applicable privacy laws for releasing data, a variety of techniques are applied while releasing information about data.


## Filtering
- Remove data a field that can uniquely identify a person, i.e. *birth date*.
- Remove data fields that in combination can uniquely identify a person, i.e. *time of arrival, gender, age, marital status* 
## Generalization 
- Instead of removing potentially identifying fields, the controller or processsor can use general terms, *birth year instead of birthdate* to protect privacy.

## Agrggregation
- Release overall statistics about distribution of data instead of original elements.

## Interactive 
- Administrators answer directed questions on behalf of researchers, instead of releasing data in its entirety; 

## Differential
- adding carefully calibrated noise to the data.

# Limitations

Utility-Privacy trade-off is a fundamental struggle between learning from data and protecting privacy. Aggressive anonymiztion significanlty reduces the data potential for conducting meaningful research.

The advantages of anonymization and psudonymization have been acknowleded widely due to the practicalility within legal frameworks. However, achieving absolute anonymization is still fraught with challenges and set backs.
The deanonymization or reidentifycation of a person from anonymysed data has been contested with many scientific studies. Starting with Paul Ohm's [article](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1450006), the discourse and critic of foolproof anonymization is gaining significant momentum.

## Famour Anonymiztion Failures

Read more about large scale failures of privacy protection by anonymization.

### AOL Search Strings
### GIC Insurance Medical records
### Netflix User data

# Conclusion
The demand for improving anonymization techiques to protect privacy has gained tremendous momentum and resultingly creating business oppertunities for data based enterprises. On the other hand, research on adversarial attacks to reidentify individuals from the anonymyzed data has seen exemplary progress. Exponential growth of data volume has made the data mining an essential need for policy guidance, private business and public good. It remains to be seen how technology progress will help balance the scale between depressing privacy risks and endless intelligence rewards possible through data mining.


# References
1. [Privacy Act, Canada](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/02_05_d_15/#heading-0-0-2-1)
2. [PIPEDA, Canada](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/)
3. [GDPR Recital26](https://gdpr-info.eu/recitals/no-26/)
4. [Anonymization Primer](https://iapp.org/news/a/looking-to-comply-with-gdpr-heres-a-primer-on-anonymization-and-pseudonymization/)
5. [No Silver Bullet](http://randomwalker.info/publications/no-silver-bullet-de-identification.pdf)
6. [Robust De-anonymization of Large Sparse Datasets](https://www.cs.utexas.edu/~shmat/shmat_oak08netflix.pdf)
7. [Broken Promises of Privacy: Responding to the Surprising Failure of Anonymization](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1450006)
8. [GDPR definition of Personal Data](https://gdpr-info.eu/issues/personal-data/)
9. [Recital 28: pseudonymisation](https://gdpr-info.eu/recitals/no-28/)
10. [The Netflix Prize](http://www.netflixprize.com/rules)

