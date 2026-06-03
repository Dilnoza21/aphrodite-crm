# Unit 6: Networking in the Cloud — Task 1 Report

**Business use case:** A wholesale ready-made clothing company migrating its **Customer Relationship Management (CRM)** system to a cloud platform.

---

## Introduction

The company is a wholesaler of ready-made clothing. Its customers are not individual shoppers but retail businesses — boutiques, high-street shops and online stores — that buy clothing in bulk to resell. To manage these business relationships, the company relies on a **CRM system**, which stores every customer's account details, order history, sales-representative notes, support requests and marketing activity.

At present this CRM runs on a single physical server located inside the company's head office, an arrangement known as an **on-premises** system. As the business has grown, the number of staff and customers using the CRM has increased, and the ageing local server can no longer cope with the demand. Management therefore wishes to migrate the CRM to a **cloud platform**, meaning the computing power, storage and networking are rented from a large provider such as Amazon Web Services, Microsoft Azure or Google Cloud and accessed over the internet rather than owned and maintained on site.

This report examines how that migration affects the business, explains the core concepts and components of cloud networking, compares the available service models and network services, and justifies the move with reference to cost, security, scalability and continuity.

---

## 1. The effect of cloud-based remote services and network connections on the business

Moving the CRM into the cloud changes far more than where the data is stored; it changes how the company works each day, how productive its staff can be, and the quality of service its customers receive.

### Effect on daily operations

When the CRM is hosted in the cloud, it can be reached from any location with an internet connection rather than only from inside the head office. This has a direct effect on the company's everyday activities. A sales representative visiting a boutique can open the customer's full order history on a tablet while standing in the shop, confirm stock availability and place a repeat order immediately, instead of having to telephone the office and wait for someone to look up the record. Warehouse staff can update order status from the warehouse floor, and that update is instantly visible to the sales and customer-service teams. Because every department works from the same live information, the delays and miscommunication that occur when data is locked inside one office server are removed.

A useful comparison is the situation before and after migration. With the old on-premises system, if the office server was switched off in the evening or failed during the day, no remote work was possible and the business effectively stopped. With a cloud-hosted CRM, the system is available continuously and from anywhere, so daily operations are no longer tied to one building or one machine.

### Effect on employee productivity

Remote access through the cloud removes much of the waiting and duplication that slow staff down. Previously, a sales representative away from the office might write order details on paper and re-enter them later, creating extra work and the risk of mistakes. With cloud access, information is entered once, in real time, and is immediately correct for everyone. Staff also spend less time dealing with technical problems, because the cloud provider maintains the underlying hardware; if a server fails, the provider replaces it without the company's small IT team needing to intervene.

There is, however, a balanced point worth making. Cloud productivity depends entirely on a reliable internet connection. If the office connection is slow or fails, staff cannot reach the CRM at all, whereas the old local server would still work within the building. For this reason, productivity gains are real but conditional on the company maintaining good, ideally backed-up, internet connectivity.

### Effect on the quality of service provided to customers

For a wholesaler, the quality of service depends on responding to customers quickly and accurately. A cloud-hosted CRM improves this in several ways. Because staff can see a customer's complete history instantly, they can answer queries on the first call rather than promising to ring back. Because the system scales during busy periods, it does not slow down when many staff are placing seasonal orders at once, so customers are served at the same speed in peak season as in quiet months. And because the data is held centrally and consistently, customers are not given contradictory information by different members of staff.

For example, during a seasonal clothing launch, dozens of retail customers may place large orders within the same few days. On the old single server this surge would slow the CRM to a crawl, frustrating both staff and customers. In the cloud, additional capacity is added automatically to absorb the surge, so service quality is maintained exactly when it matters most.

---

## 2. Fundamental concepts, architecture and core components of cloud networking

Before designing a cloud solution it is necessary to understand the building blocks of a cloud network and how they fit together. The following components form the architecture that will host the CRM.

**Virtual Private Cloud (VPC).** A VPC is a private, isolated section of the cloud provider's data centre that belongs only to our company. It can be pictured as a fenced-off plot of land rented inside an enormous shared estate: although the provider's hardware is shared by many customers, our VPC is logically separated so that no other tenant can see or reach our resources. The company's CRM servers and database all live inside this VPC.

**Subnet.** A subnet is a smaller division within the VPC, created so that resources can be grouped according to their purpose. Subnets are described as either public or private. A **public subnet** can communicate with the internet and is used for components that must be reachable from outside, such as the part of the system that receives users' web requests. A **private subnet** has no direct route to the internet and is used for sensitive components, such as the CRM application servers and the customer database, keeping them hidden from outside attackers.

**Routing table.** A routing table is a set of rules that decides where network traffic is sent next, much like a signpost at a junction. Each subnet is associated with a routing table that tells traffic, for example, "to reach the internet, go through the internet gateway" or "to reach the database subnet, stay inside the VPC." Correct routing is what keeps traffic flowing to the right place and prevents private resources from accidentally being exposed.

**Gateway.** A gateway is a controlled doorway between two networks. The **internet gateway** is the doorway between the VPC and the public internet; it allows the CRM's public-facing component to receive requests from staff and customers. Without an internet gateway, the VPC would be completely sealed off.

**NAT (Network Address Translation) gateway.** A NAT gateway allows resources in a private subnet to start outbound connections to the internet — for example, a CRM server downloading a security update — while preventing anyone on the internet from starting a connection inward. It can be thought of as a one-way door: staff inside can reach out, but strangers outside cannot come in. This lets private servers stay updated and protected at the same time.

**Firewall (security groups).** A firewall is a filter that allows or blocks network traffic according to defined rules. In cloud platforms this is usually implemented as "security groups" attached to each resource. A typical rule for the CRM would permit only encrypted web traffic (HTTPS on port 443) to reach the public-facing servers and block everything else, sharply reducing the ways an attacker could get in.

**Load balancer.** A load balancer sits in front of several servers and distributes incoming requests evenly between them, so that no single server becomes overwhelmed. If one server fails, the load balancer simply stops sending traffic to it and uses the others, which keeps the CRM available.

**DNS (Domain Name System).** DNS translates a human-friendly web address such as `crm.clothingco.com` into the numeric IP address that computers use to locate the service. It means staff can reach the CRM by typing a memorable name, and the address can remain the same even if the servers behind it are replaced.

Taken together, these components form a layered architecture: requests enter the VPC through the internet gateway, are shared out by the load balancer in the public subnet, and are handled by application servers and a database that sit protected in private subnets, with firewalls, routing tables, NAT and DNS all working together to keep the system secure, reachable and reliable.

---

## 3. Comparative analysis of cloud service models and network-level services

### Cloud service models: IaaS, PaaS and SaaS

Cloud services are offered at three different levels, depending on how much of the system the provider manages and how much the customer manages. The common analogy is pizza: making it entirely at home, buying a take-and-bake, or having it delivered — in each case more of the work is done for you.

**Infrastructure as a Service (IaaS)** provides the basic building blocks — virtual servers, storage and networking — which the customer then configures and manages. The provider looks after the physical hardware; the company installs and maintains the operating system, the CRM software and everything above it. This gives the most control and flexibility but requires the most technical skill and effort.

**Platform as a Service (PaaS)** provides a ready-made environment in which to run applications, including the operating system and supporting software, so the company only has to deploy and manage its own application. This removes much of the routine maintenance but offers less control over the underlying setup.

**Software as a Service (SaaS)** provides a complete, finished application that the company simply uses through a web browser, with the provider managing everything beneath it. There is almost no maintenance burden, but also the least flexibility, because the company cannot deeply customise how the software works.

| Aspect | IaaS | PaaS | SaaS |
|---|---|---|---|
| Customer manages | OS, software, application, data | Application and data only | Data only (just uses the app) |
| Provider manages | Physical hardware and network | Hardware, OS, runtime | Everything |
| Control | Highest | Medium | Lowest |
| Maintenance effort | Highest | Medium | Lowest |
| Best suited to | A custom CRM the company wants to control | Running custom CRM code without managing servers | Renting a ready-made CRM product |

For this company, an **IaaS or PaaS** approach is most appropriate if it wishes to host and control its own CRM, because it can design the network (VPC, subnets, load balancing) to suit its needs. A SaaS CRM would be the simplest option but would give the company less control over its data and configuration, which matters where customer information must be carefully protected.

### Network-level services: Load Balancer, VPN and CDN

These three services operate at the network level and each solves a different problem, so they are best understood by comparison rather than in isolation.

A **Load Balancer** distributes incoming traffic across multiple servers. Its purpose is performance and availability: it prevents any one server from being overloaded and keeps the CRM running even if a server fails. For the clothing company it is essential during seasonal order surges, when traffic to the CRM rises sharply.

A **Virtual Private Network (VPN)** creates an encrypted tunnel across the public internet so that data travels securely between two points. Its purpose is security of connection. It allows the head office and regional warehouses to connect to the cloud CRM as though they were on the same private network, and allows remote sales staff to connect safely from outside.

A **Content Delivery Network (CDN)** stores copies of content in many locations around the world and serves each user from the nearest one. Its purpose is speed and reduced load: by delivering images, pages and files from a nearby location, it makes the system feel faster and takes pressure off the main servers.

| Service | Main purpose | What it improves | CRM example |
|---|---|---|---|
| Load Balancer | Share traffic across servers | Availability and performance under load | Spreading seasonal order traffic across several CRM servers |
| VPN | Encrypted private connection | Security of data in transit | Linking warehouses and remote reps securely to the cloud CRM |
| CDN | Serve content from nearby locations | Speed and reduced server load | Delivering CRM images/files quickly to staff in different regions |

The key comparative point is that these services are complementary rather than alternatives: the load balancer keeps the CRM responsive under heavy use, the VPN keeps the connections to it secure, and the CDN keeps it fast for geographically spread users. A well-designed cloud CRM would use all three together.

---

## 4. Justification for migrating to a cloud network environment

The decision to migrate can be justified against four measures that matter most to management: cost, security, scalability and continuous operation.

**Cost.** With the on-premises system, the company faced large, irregular spending: buying servers outright, paying for their installation, electricity and cooling, and replacing them every few years whether or not they were fully used. A cloud model replaces this with a pay-as-you-use arrangement, where the company pays only for the capacity it actually consumes and avoids large upfront purchases. The evidence for this benefit is the seasonal nature of the business: demand peaks for only part of the year, so paying year-round for hardware sized to the busiest week is wasteful, whereas the cloud allows capacity (and cost) to rise and fall with demand. The honest qualification is that cloud costs must be monitored, because resources left running unnecessarily can cause spending to creep upward.

**Security.** A cloud network allows a stronger security design than a single office server. The customer database can be hidden in a private subnet with no direct internet route, firewalls can restrict traffic to only encrypted web requests, and VPNs can encrypt all remote access. The evidence here is the layered architecture described in section 2: an attacker would have to pass through several independent barriers rather than reach a single exposed machine. The qualification is that security in the cloud is shared: the provider secures the physical hardware, but the company must configure its subnets, firewalls and access rules correctly, so the main remaining risk shifts from hardware failure to human misconfiguration.

**Scalability.** This is the clearest justification of all. The old single server had a fixed capacity that could not grow with the business, and during peak periods it slowed down or failed. A cloud environment can add servers automatically when demand rises and remove them when it falls, with a load balancer spreading the work between them. The evidence is straightforward: the existing server already cannot meet current demand, so a system that grows on its own directly solves the problem that prompted the migration.

**Continuous operation.** A cloud CRM can be run across several of the provider's data centres at once, so that if one location has a problem the system continues running from another. Backups and recovery are also faster and more automatic than with a single physical server. The evidence is the cost of downtime to the business: when the office server failed, the whole company lost access, but a multi-location cloud design keeps the CRM available even during a partial failure. The qualification is that continuity now depends on the company's internet connection, so a backup connection is a sensible investment.

Taken together, these four measures justify the migration. The gains in scalability, cost-efficiency and continuity directly address the problems of the current system, and the security design is stronger overall, provided it is configured carefully and supported by a reliable internet connection.

---

## 5. Deploying a dynamic website in the cloud using network services

To demonstrate cloud networking in practice, a dynamic website (representing the CRM's web interface) is deployed inside the cloud environment and made reachable using the network components described earlier. A dynamic website differs from a static one in that its pages are generated in response to user input — for example, showing a particular customer's order history rather than a fixed page — which is exactly how a CRM behaves.

The deployment brings the earlier concepts together in a working arrangement. First, a **VPC** is created to hold the whole system, and within it a **public subnet** and a **private subnet** are defined. The web/application server that runs the dynamic site is placed in the private subnet so that it cannot be reached directly from the internet. A **load balancer** is placed in the public subnet to receive incoming requests and forward them to the application server. An **internet gateway** is attached to the VPC so that the load balancer can be reached from outside, and a **NAT gateway** is added so the private server can download updates without being exposed. The **routing tables** are configured so that public traffic flows through the internet gateway while internal traffic stays within the VPC. A **firewall/security group** is set to allow only encrypted HTTPS traffic to the load balancer. Finally, **DNS** is configured so the site can be reached by a readable address such as `crm.clothingco.com`.

When a user opens that address, the request is resolved by DNS, enters through the internet gateway, is received by the load balancer, and is passed to the application server in the private subnet, which generates the page and returns it. The result is a working dynamic website that is publicly reachable yet keeps its application server and data protected — a small-scale model of how the real CRM would run.

> Practical note: this part of the task must be carried out and evidenced with your own screenshots — the VPC and subnet configuration, the load balancer, the security group rules, and the live site loading in a browser. The text above explains what each step achieves so that the screenshots can be described and justified clearly.

---

## 6. Implementing a CI/CD pipeline with auto-scaling and load balancing

The final practical element demonstrates how the deployed system is kept up to date automatically and how it copes with sudden heavy demand.

**Continuous Integration and Continuous Deployment (CI/CD)** is an automated process for delivering changes to the application. *Continuous Integration* means that whenever a developer makes a change to the website's code and saves it to a shared repository, the change is automatically tested. *Continuous Deployment* means that, once the tests pass, the change is automatically published to the live cloud environment without anyone having to copy files by hand. The benefit is speed and reliability: updates to the CRM — such as a new order-entry feature — reach users quickly and with fewer mistakes, because the repetitive, error-prone manual steps are removed. For example, a change committed in the morning can be tested and live the same afternoon, automatically.

**Auto-scaling** is the mechanism that adds or removes servers in response to demand. A rule is set so that when the servers become busy — for instance, when their processor usage rises above a chosen level during a seasonal order surge — the cloud automatically launches additional copies of the application server. When demand falls again, the extra servers are removed so the company stops paying for them. This directly solves the problem of the old fixed-capacity server, which could neither grow during peaks nor shrink during quiet times.

**Load balancing** works hand in hand with auto-scaling. As new servers are created, the load balancer automatically begins sharing incoming requests across all of them, so the extra capacity is actually used and no single server is overwhelmed. If a server fails or is removed, the load balancer simply stops sending traffic to it.

The two mechanisms are best understood together through an example. Imagine a major seasonal launch where hundreds of retail customers place orders in a short time. As traffic to the CRM rises, the busy servers trigger the auto-scaling rule, which launches several more application servers. The load balancer immediately distributes the flood of requests across the enlarged group of servers, so each one handles only a manageable share and the CRM stays fast and responsive. Once the launch is over and traffic subsides, auto-scaling removes the extra servers, returning the company to its normal, lower running cost. This combination of CI/CD, auto-scaling and load balancing is what allows a cloud-hosted CRM to be updated continuously and to remain reliable under exactly the conditions that would have overwhelmed the old on-premises system.

> Practical note: a high-load test (for example, generating many simultaneous requests) should be run and evidenced with screenshots showing the extra servers being created and the load balancer distributing traffic, so that the behaviour described above is demonstrated rather than only explained.
