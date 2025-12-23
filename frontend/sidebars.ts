import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Textbook Chapters',
      items: [
        'chapter-01-foundations',
        'chapter-02-ros2',
        'chapter-03-gazebo',
        'chapter-04-isaac',
        'chapter-05-vla',
        'chapter-06-capstone',
      ],
    },
  ],
};

export default sidebars;
