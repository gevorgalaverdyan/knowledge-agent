import { ApplicationConfig, inject, PLATFORM_ID, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideMarkdown } from 'ngx-markdown'
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideZard } from '@/shared/core/provider/providezard';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { authHttpInterceptorFn, provideAuth0 } from '@auth0/auth0-angular';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withFetch(), withInterceptors([authHttpInterceptorFn])),
    provideMarkdown(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideZard(),
    provideAuth0({
      domain: 'dev-5xkzrksvvdyocvxg.us.auth0.com',
      clientId: 'ORZEjOZ28svXnpdx0gB2QMgchMGVLSrZ',
      authorizationParams: {
        audience: 'https://dev-5xkzrksvvdyocvxg.us.auth0.com/api/v2/',
        redirect_uri: typeof window !== 'undefined' ? window.location.origin : 'http://localhost:4200'
      },
      httpInterceptor: {
        allowedList: [
          {
            uri: 'http://localhost:8000/*',
            tokenOptions: {
              authorizationParams: {
                audience: 'https://dev-5xkzrksvvdyocvxg.us.auth0.com/api/v2/'
              }
            }
          }
        ]
      }
    }),
  ]
};
