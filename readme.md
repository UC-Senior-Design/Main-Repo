# Senior Design GPS Deprived Localization Research Project 2019/2020

- [Senior Design GPS Deprived Localization Research Project 2019/2020](#senior-design-gps-deprived-localization-research-project-20192020)
  - [Demo](#demo)
  - [Senior Design Poster](#senior-design-poster)
  - [Project Abstraction](#project-abstraction)
    - [Team](#team)
  - [Project Description](#project-description)
  - [Final Presentation PowerPoint](#final-presentation-powerpoint)
  - [Final Self Assessments](#final-self-assessments)
    - [Joseph Krusling](#joseph-krusling)
    - [Tanner Bornemann](#tanner-bornemann)
  - [User Stories & Design Diagrams](#user-stories--design-diagrams)
  - [Project Tasks & Timeline](#project-tasks--timeline)
  - [Project Presentation](#project-presentation)
  - [Capstone Assessments](#capstone-assessments)
  - [Professional Biographies](#professional-biographies)
  - [Budget](#budget)
  - [Appendix](#appendix)
    - [Research](#research)
      - [Papers](#papers)

## Demo

[![Demo of localization](demo.gif)](https://www.youtube.com/watch?v=M_b4fiXxZLQ)

## Senior Design Poster

[Senior Design Poster](https://github.com/UC-Senior-Design/Main-Repo/blob/master/SeniorDesignPosterDraft.pdf)

## Project Abstraction

Unmanned aerial vehicles rely principally on GPS for localization and navigation, so
GPS-deprived environments pose a major challenge. We seek to explore and
implement various strategies for automating UAV flight without access to GPS. The
first strategy entails the use of many fixed cameras placed in the environment, which
identify the location of the UAV through the fusion and analysis of their individual
camera feeds. The second strategy uses WiFi signals obtained from numerous access
points and analyses the relative signal strengths to localize the UAV. These
strategies will be used simultaneously to achieve robust localization.

### Team

- Matthew Manley - manleymj@mail.uc.edu
- Joseph Krusling - kruslijm@mail.uc.edu
- Tanner Bornemann - bornemtr@mail.uc.edu
- Mahdi Norouzi - norouzmi@ucmail.uc.edu (Faculty Advisor)

## Project Description

[Project Description can be found here](https://github.com/UC-Senior-Design/Main-Repo/wiki/Project-Description)

[Project Description Video](https://www.youtube.com/watch?v=YBAmAesEE_g)

## Final Presentation PowerPoint

[Final Presentation Slides](https://docs.google.com/presentation/d/16rOYFmPqiy3v9u1N-_m7KnntrKwo8C93bKVkQVXkits/edit?usp=sharing)

## Final Self Assessments

### Joseph Krusling

My primary contribution to the project was designing and programming the optical drone tracking system. I developed the computer vision code which could detect the drone (or training marker) in a series of images, as well as the feed-forward neural network which mapped a set of drone positions in 2D space into a position in 3D space. Combined, these components form a system that allows for a drone to be tracked in real time. We consider this system to be extremely successful. While it's only a prototype, we achieved impressive accuracy and precision using only consumer-grade cameras and compute. I believe that our system can be scaled up to serve useful real-world applications that involve object localization.


My biggest obstacle was finding comparable research. What we're doing is somewhat novel, so we had to draw a wide net and combine tools and ideas from multiple places. While I'm overjoyed with where our team ended up at the end of the project, the path to get here was beset on all sides by knowledge gaps, frustration, and doubts about whether we were pursuing the right problem. Last semester I identified that one of my greatest strengths is the ability to learn new tools while on the job. Since I came into this project with very little computer vision experience, this skill was essential for developing the knowledge needed to develop the tracking system. This semester taught me so much about machine learning and computer vision, but I still know a very small fraction of what I want to.

### Tanner Bornemann

My individual contribution was mostly the research done on Wi-Fi RSSI Localization. This consisted of identifying how others have used RSSI for localization in the past and if it was possible to use or to build onto what others have done for our project. I eventually came to the conclusion that RSSI localization was not usable for our goal of GPS Deprived UAV Localization. After this was completed I worked on the implementation of the Optical Localization we use in our final project demonstration.


The majority of my obstacles were finding research on Wi-Fi RSSI Localization and understanding the existing research. Then trying to figure out if we can apply what I learned to our end goal. I learned a lot through applying the actual research and was surprised by my ability to read academic papers on the subject. This wasn’t something I was good at early in my academic career.

## User Stories & Design Diagrams

[User Stories can be found here](https://github.com/UC-Senior-Design/Main-Repo/wiki/User-Stories)

[Design Diagrams can be found here](https://github.com/UC-Senior-Design/Main-Repo/blob/master/hw/design_diagrams/Design%20Diagrams.pdf)

## Project Tasks & Timeline

[Task list can be found here](https://github.com/UC-Senior-Design/Main-Repo/wiki/Task-List)

[Timeline can be found here](https://github.com/UC-Senior-Design/Main-Repo/wiki/Milestones)

## Project Presentation

[PPT presentation can be found here](https://github.com/UC-Senior-Design/Main-Repo/blob/master/hw/GPS%20Deprived%20UAV%20Localization.pdf)

## Capstone Assessments

[Assessments can be found here](https://github.com/UC-Senior-Design/Main-Repo/tree/master/hw/capstone_assessment)

## Professional Biographies

[Biographies can be found here](https://github.com/UC-Senior-Design/Main-Repo/tree/master/hw/bios)

## Budget

TODO

- Raspberry Pi 4 bundle https://vilros.com/collections/raspberry-pi-kits/products/vilros-raspberry-pi-4-model-b-basic-starter-kit-with-fan-cooled-clear-transparent-case?variant=29406580080734
- Raspberry Pi GPS Logger https://www.adafruit.com/product/746
- Raspberry Pi Battery Pack https://www.adafruit.com/product/4288
- 3x Logitech HD WebCam C920 https://smile.amazon.com/Logitech-Widescreen-Calling-Recording-Desktop/dp/B006JH8T3S
- Drone?
- Flex?

## Appendix

### Research

#### Papers

Mendeley Group: https://www.mendeley.com/community/gps-deprived-drones/

- Decimeter-Level Localization with a Single WiFi Access Point (Vasisht D Kumar S Katabi D)
- Multi-camera sensor system for 3D segmentation and localization of multiple mobile robots (Losada C Mazo M Palazuelos S Pizarro D Marrón M)
- Marker localization with a multi-camera system (Szaloki D Koszo N Csorba K Tevesz G)
- Efficient Optical Flow and Stereo Vision for Velocity Estimation and Obstacle Avoidance on an Autonomous Pocket Drone (McGuire K De Croon G De Wagter C Tuyls K Kappen H)
- Obstacle Avoidance Strategy using Onboard Stereo Vision on a Flapping Wing MAV (Tijmons S De Croon G Remes B De Wagter C Mulder M)
- CNN-SLAM: Real-time dense monocular SLAM with learned depth prediction (Tateno K Tombari F Laina I Navab N)
- A pure vision-based approach to topological SLAM (Lui W Jarvis R)
- Real-time 3D reconstruction on construction site using visual SLAM and UAV (Shang Z Shen Z)
- LSD-SLAM: Large-Scale Direct monocular SLAM (Engel J Schöps T Cremers D)
- SLAM and obstacle detection for tall autonomous robotic medical assistant (Zukowski M Matus K Kamienski D Kondratiuk M Ambroziak L Kuc B)
- ORB-SLAM2: An Open-Source SLAM System for Monocular, Stereo, and RGB-D Cameras (Mur-Artal R Tardos J)
- Monocular visual SLAM for small UAVs in GPS-denied environments (Wang C Wang T Liang J Chen Y Zhang Y Wang C)
- A Kinect-based indoor mobile robot localization (Hamzeh O Elnagar A)
- Indoor Dense Depth Map at Drone Hovering (Saha A Maity S Bhowmick B)
- Evaluating SLAM approaches for microsoft kinect (Schindhelm C)
- An MAV Localization and Mapping System Based on Dual Realsense Cameras (Bi Y Li J Qin H Lan M Shan M Lin F Chen B)
- SLAM with D435i (Dorodnicov S)
- Autonomous Flight in Unknown Indoor Environments (Bachrach A He R Roy N)
- RANGE-Robust autonomous navigation in GPS-denied environments (Bachrach A Prentice S He R Roy N)
- Visual 3-D SLAM from UAVs (Artieda J Sebastian J Campoy P Correa J Mondragón I Martínez C Olivares M)
- Estimation, planning, and mapping for autonomous flight using an RGB-D camera in GPS-denied environments (Bachrach A Prentice S He R HenrY. P Huang A KrainiN. M Maturana D Fox D Roy N)
- SVO: Semidirect Visual Odometry for Monocular and Multicamera Systems (Forster C Zhang Z Gassner M Werlberger M Scaramuzza D)
- Cooperative monocular-based SLAM for multi-UAV systems in GPS-denied environments (Trujillo J Munguia R Guerra E Grau A)
- Fast, autonomous flight in GPS-denied and cluttered environments (Mohta K Watterson M Mulgaonkar Y Liu S Qu C Makineni A Saulnier K Sun K Zhu A Delmerico J Karydis K Atanasov N Loianno G Scaramuzza D Daniilidis K Taylor C Kumar V)
- Guidance and control for a mars helicopter (Grip H Scharf D Malpica C Johnson W Mandić M Singh G Young L)
