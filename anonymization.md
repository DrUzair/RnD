# Data Anonymization

Data anonymization, also known as psudeonymization, refers to a family of techniques that make it impossible or impractical to identify a data subject.

Compliance to General Data Protection Regulation (**GDPR**) has increased the importance of data anonymization because GPPR relaxes it stringent requirements if effective measures are taken to de-identify the people in data. If executed properly, the regulations allow processing, storage and communication of anonymized data.

GDPR defines anonymized data as “information which does not relate to an identified or identifiable natural person or to personal data rendered anonymous in such a manner that the data subject is not or no longer identifiable.”

## **[GDPR Recital 26](https://gdpr-info.eu/recitals/no-26/)** 

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

## [Pseudonymisation](https://gdpr-info.eu/recitals/no-28/)

Pseudonymisation is the process and techniques of de-identifying personal data by substituting it with psuedo information that allows analysis and processing but a natural person can not be identified with that information. It is not as strict as anonymization. Pseudonymizing creates a new attribute that link personal identifiers with psuedonymized data to enable de-anonymization later. The links then become a proxy for real information and get protected by the data controllers while transformed data can be *legaly* stored, processed and transfered.

GDPR recital 28 notes as following:

*The application of pseudonymisation to personal data can reduce the risks to the data subjects concerned and help controllers and processors to meet their data-protection obligations. 
2. The explicit introduction of ‘pseudonymisation’ in this Regulation is not intended to preclude any other measures of data protection.*


# Limitations and Threats
The advantages of anonymization and psudonymization have been acknowleded widely due to the practicalility within legal frameworks. However, achieving absolute anonymization is still fraught with challenges and set backs.
The deanonymization or reidentifycation of a person from anonymysed data has been contested with many scientific studies. Starting with Paul Ohm's [article](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1450006), the discourse and critic of foolproof anonymization is gaining significant momentum.



# References
1. [Recital26](https://gdpr-info.eu/recitals/no-26/)
2. [Primer](https://iapp.org/news/a/looking-to-comply-with-gdpr-heres-a-primer-on-anonymization-and-pseudonymization/)
3. [No Silver Bullet](http://randomwalker.info/publications/no-silver-bullet-de-identification.pdf)
4. [Robust De-anonymization of Large Sparse Datasets](https://www.cs.utexas.edu/~shmat/shmat_oak08netflix.pdf)
5. [Broken Promises of Privacy: Responding to the Surprising Failure of Anonymization](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1450006)
6. [GDPR definition of Personal Data](https://gdpr-info.eu/issues/personal-data/)
7. [Recital 28: pseudonymisation](https://gdpr-info.eu/recitals/no-28/)
