# Classifying Pitch Types

This is the first project within this repository that I'm getting to after setting up the database.

## 1. Clarify the problem and constraints

Given ball flight metrics, can a ML model predict what kind of pitch is being thrown?

Traditional pitches known as 2-seams are now typically labeled as sinkers across the board for pitchers in the MLB.  Does the 2-seam fastball even exist anymore or has a labeling change occurred? Similar labeling customs have evolved regarding sliders and supinated off speed pitches with the introduction of the sweeper label, to account for sliders with more lateral movement bias than the traditional slider.  I find this labeling to be an interesting classification problem surrounding pitch design and how pitchers talk about their repertoires.

This kind of model is employed very regularly, and is present during every game that is televised, both live at the stadium on stadium screens, and up in the score bug on television displaying what kind of pitch was just thrown.  

Target Variable: Pitch Type

Looking through Driveline blogs I stumbled upon this link(https://www.drivelinebaseball.com/2019/03/deeper-dive-offspeed-pitches-pitch-classification/?nab=1) that goes over pitch typing for offspeed pitches, but provides some very useful tables that we can use for validation of our classifiers.



Some examples of clustering methods used that were mentioned(in that article and linked articles) were 

 - K-means clustering
 - Hierarchical clustering
 - Gaussian Mixture models(using mclust - R library)


## 2. Establish metrics

MLB:
pitch_type - The type of pitch derived from Statcast.
FF - 4-Seam Fastball
CH - Changeup
CU - Curveball
FC - Cutter
EP - Eephus
FO - Forkball
KC - Knuckle Curve
KN - Knuckleball
PO - Other
PO - Pitch Out
SC - Screwball
SI - Sinker
SL - Slider
CS - Slow Curve
SV - Slurve
FS - Split-Finger
ST - Sweeper

release_speed - Pitch velocities from 2008-16 are via Pitch F/X, and adjusted to roughly out-of-hand release point. All velocities from 2017 and beyond are Statcast, which are reported out-of-hand.

release_pos_x - Horizontal Release Position of the ball measured in feet from the catcher's perspective.

release_pos_z - Vertical Release Position of the ball measured in feet from the catcher's perspective.

player_name - Player's name tied to the event of the search.

pitcher - MLB Player Id tied to the play event.

description - Description of the resulting pitch.

zone - Zone location of the ball when it crosses the plate from the catcher's perspective.

p_throws - Hand pitcher throws with.

pfx_x - Horizontal movement in feet from the catcher's perspective.

pfx_z - Vertical movement in feet from the catcher's perpsective.

plate_x - Horizontal position of the ball when it crosses home plate from the catcher's perspective.

plate_z - Vertical position of the ball when it crosses home plate from the catcher's perspective.

vx0 - The velocity of the pitch, in feet per second, in x-dimension, determined at y=50 feet.

vy0 - The velocity of the pitch, in feet per second, in y-dimension, determined at y=50 feet.

vz0 - The velocity of the pitch, in feet per second, in z-dimension, determined at y=50 feet.

ax - The acceleration of the pitch, in feet per second per second, in x-dimension, determined at y=50 feet.

ay - The acceleration of the pitch, in feet per second per second, in y-dimension, determined at y=50 feet.

az - The acceleration of the pitch, in feet per second per second, in z-dimension, determined at y=50 feet.

effective_speed - Derived speed based on the the extension of the pitcher's release.

release_spin_rate - Spin rate of pitch tracked by Statcast.

release_extension - Release extension of pitch in feet as tracked by Statcast.

pitcher - MLB Player Id tied to the play event.

release_pos_y - Release position of pitch measured in feet from the catcher's perspective.

pitch_name - The name of the pitch derived from the Statcast Data.

spin_axis - The Spin Axis in the 2D X-Z plane in degrees from 0 to 360, such that 180 represents a pure backspin fastball and 0 degrees represents a pure topspin (12-6) curveball


SELECT ps.pitcher, ps.player_name, ps.pitch_type, ps.pitch_name,ps.release_speed, ps.release_pos_x, ps.release_pos_y, ps.release_pos_z, ps.description, ps.zone, ps.p_throws, ps.pfx_x, ps.pfx_z, ps.plate_x, ps.plate_z, ps.vx0, ps.vy0, ps.vz0,ps.ax, ps.ay, ps.az, ps.effective_speed, ps.release_spin_rate, ps.release_extension, ps.spin_axis
from pitches_statcast ps
where (pitch_type = 'SI' OR pitch_type = 'FS') AND game_year < 2021;

Get plot back, execute locally - scp mikerabayda@IP:/home/mikerabayda/repos/BaseballAnalysisSite/analyses/classify_pitch_types/scatter_pitch.png .


## 3. Understand your data sources

Statcast data - MLB Statcast data from March of 2019-2024
Trackman data - NCAA

## 4. Explore your Data 

Continuous? Categorical? Ordinal?
Outliers? Mising values? Skewed Distributions?

For continuous features:
  histogram - Distributions
  boxplot - per class to see how that feature varies among labeled pitch types 
  QQ plot? - compares feature distribution to a normal distribution 

For categorical features:
  frequency counts per class 
  class balance

For relationships between features:
  correlation matrix - multicollinearity


## 5. Clean Data 

convert MLB metrics to inches

## 6. Feature Engineering

all features should be scaled
Correlation matrix should be created to identify multicollinearity
PCA may be employed depending on the features that are correlated with one another


## 7. Model Selection

Assumption Heavy models:
Logistic Regression - needs scaling, PCA 
Gaussian Naive Bayes - needs scaling, PCA, probably some log transforms
Linear Discriminant Analysis?
Gaussian Mixture Model 

Light Assumption models:
XGBoost
RFClassifier
SVM



## 8. Model Training & Evaluation
## 9. Deployment
