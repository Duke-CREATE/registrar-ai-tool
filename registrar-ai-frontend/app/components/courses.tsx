// courses.tsx
// import React, { useState } from 'react';

// // Individual Course Component
// const Course = ({ course }) => {
//   const [showDetails, setShowDetails] = useState(false);

//   const toggleDetails = () => setShowDetails(!showDetails);

//   return (
//     <div className="course">
//       <button onClick={toggleDetails} className="course-name">
//         {course['course name']}
//       </button>
//       {showDetails && (
//         <div className="course-details">
//           <p>Description: {course['course description']}</p>
//           <p>Start Time: {course['start time']}</p>
//           <p>End Time: {course['end time']}</p>
//           <p>Days Offered: {course['days offered']}</p>
//           <p>Term: {course['term']}</p>
//         </div>
//       )}
//     </div>
//   );
// };

// // Courses List Component
// export const CoursesList = ({ courses }) => {
//   return (
//     <div>
//       {Object.entries(courses).map(([courseId, courseDetails]) => (
//         <Course key={courseId} course={courseDetails} />
//       ))}
//     </div>
//   );
// };
