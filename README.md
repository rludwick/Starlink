# Starlink Beam Planner
To provide internet to a user, a satellite forms a "beam" towards that user and the user forms a beam towards the satellite. After doing this the satellite and user can form a high-bandwidth wireless link.

Starlink satellites are designed to be very flexible. For this problem, each satellite is capable of forming up to 32 independent beams simultaneously. Therefore one Satellite can serve up to 32 users. Each beam is assigned one of 4 "colors" corresponding to the frequencies used to communicate with that user.

There are a few constraints on how those beams can be placed:
From the user's perspective, the beam serving them must be within 45 degrees of vertical. Assume a spherical Earth, such that all surface normals pass through the center of the Earth (0, 0, 0).
On each Starlink satellite, no two beams of the same color may be pointed within 10 degrees of each other, or they will interfere with one another.

# Problem
Given a list of users and satellites, assign beams to users respecting the constraints above.
