# Automated-CERTIFICATE-Renewal-System
Enterprise Certificate Renewal Utility, that makes the certificate renewal process quite easy and manageable.
Certificates are an important piece of security identification associated to any entity that has a presence on the internet. They
play an important role by enabling a secure channel of communication between the user/customer and the omnipresent Business entity.

In an enterprise scenario, which has many such interaction endpoints, the manageability aspect could be quite overwhelming. As is
the norm, each of the user/customer facing (or internet exposed) applications, would be having a certificate issued to them to perform
the above mentioned, safe interation on the web.

## Where lies the problem?
The certificate Renewal process tends be very cumbersome, and especially in an Enterprise scenario, where we may have many
certificates issued to websites, and there are many more thousand websites which will have many more certificates
altogether. It can be as difficult as doing the below.
> Counting stars using your fingers.

In my project, we keep track of the certificates exipring over time, and would renew it manually (say two months before) when
it is due to expire. The problem arises as the project grows, when you have multiple functional, high-traffic websites and you need
to renew their certificates before it has any business impact. The process is quite straightforward, but monotonous.

This looks like an *`Automation`* Problem.

__Note:__ We use `OpenSSL` to generate the *Private Key* and *CSR* before submitting it to the Certificate Authority of our choice.

## The Software
This is where the __Renewal Utility__ comes to the rescue. With help of this utility, the renewal process is as easy as changing
certain configuration settings and running the program. The utility takes care of the rest.

- [x] Generating the Private Key
- [x] Generating the CSR (Certificate Signing Request)
  - The utility can also generate a CSR from an existing private key (If it is present).
  - Say, the CSR was created manually or by the utility (and then it crashed), it just takes over from there!!!
- [x] Submitting the CSR to the CA on their portal, and also auto-providing the other relevant details required for proper submission.

The benefits of having an automated utility is that one doesn't need to bother about the details of cetificate generation or the
commands required to generate a CSR and Private Key. This also reduces the chances of human error, while performing the process.
Also, one doesn't need to manually go the CA Portal to submit the CSR, which itself is another set of steps that require caution
and full attention.

## Winds of Change
The entire utility depends on the input configuration options (which also can be changed). You do not need to change anything in
the software, but direct the software based on those configuration options.

The configuration files can be located under the utility's root. The container folder is named __`config`__.

The only files that need to be altered per run are:
```
|---config
    ---CSRConfig
    ---PortalConfig
```

The above two files contain information that vary from certificate to certificate. I have marked the section (as *** VARIABLE SECTION ***) where those variables are grouped together for the ease of modifying.

__Note:__ Only make changes to those grouped configuration options. The rest remains the same for all the instances of the process.

## About the Environment (Requisites)
- The utility uses Python 3 (==3.4.3).
- Additional Modules include,
     - [x] Requests: HTTP for Humans
     - [x] BeautifulSoup: Webscraping made easy

## After Effect
With this utility in place, we have seen quite an improvement in the ability to manage certificate renewals within the organization.
What used to take up much of the valuable *employee time*, now can just be initiated using a program, and the rest just follows.
No special knowledge is required to run the process through the finish line. One just needs to acquaint themselves with the
utility and need to know the changes to be done at the configuration level, and thats all. The rest is taken care of.

__`That's one small step for Automation, one giant leap for my Organization.`__
