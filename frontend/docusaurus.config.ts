import type { Config } from '@docusaurus/types';
import type { Options } from '@docusaurus/preset-classic';
import { themes } from 'prism-react-renderer';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Textbook Platform',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-domain.com',
  // Set the /<baseUrl>/ to <repoPath>/ for GitHub Pages
  baseUrl: '/',

  // GitHub Pages deployment config (if using)
  organizationName: 'your-org',
  projectName: 'ai-textbook-platform',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  onDuplicateRoutes: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/docs',
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: ['./src/css/custom.css'],
        },
      } satisfies Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Chapters',
        },
        {
          href: 'https://github.com/your-org/ai-textbook-platform',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Chapters',
          items: [
            { label: 'Chapter 1: Physical AI Foundations', to: '/docs/chapter-01-foundations' },
            { label: 'Chapter 2: ROS 2', to: '/docs/chapter-02-ros2' },
            { label: 'Chapter 3: Gazebo & Digital Twins', to: '/docs/chapter-03-gazebo' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/your-org/ai-textbook-platform' },
          ],
        },
      ],
      copyright: `Built with Docusaurus. ${new Date().getFullYear()} AI Textbook Platform.`,
    },
    prism: {
      theme: themes.ocean,
      darkTheme: themes.oneDark,
      additionalLanguages: ['python', 'bash', 'yaml', 'json', 'typescript', 'jsx'],
    },
    mermaid: {
      theme: { light: 'base', dark: 'forest' },
    },
  } satisfies const,

  plugins: [
    '@docusaurus/theme-mermaid',
  ],

  // Client-side environment variables
  clientModules: [
    require.resolve('./src/clientModules.ts'),
  ],
};

export default config;
