/**
 * LanguageSwitcher Component
 *
 * Toggle between English and Urdu languages
 */

import React from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Translate from '@docusaurus/Translate';

export default function LanguageSwitcher(): React.JSX.Element {
  const { i18n } = useDocusaurusContext();
  const location = useLocation();

  const currentLocale = i18n.currentLocale;
  const locales = i18n.locales;

  // Switch language function
  const switchLanguage = (targetLocale: string) => {
    const currentPath = location.pathname;
    const pathWithoutLocale = currentPath.replace(`/${currentLocale}`, '') || '/';

    // Navigate to the same page in different language
    window.location.href = `/${targetLocale}${pathWithoutLocale}`;
  };

  return (
    <div className="language-switcher">
      {locales.map((locale) => (
        <button
          key={locale}
          onClick={() => switchLanguage(locale)}
          className={`language-button ${currentLocale === locale ? 'active' : ''}`}
          aria-label={`Switch to ${locale === 'en' ? 'English' : 'اردو'}`}
        >
          {locale === 'en' ? 'English' : 'اردو'}
        </button>
      ))}
    </div>
  );
}
