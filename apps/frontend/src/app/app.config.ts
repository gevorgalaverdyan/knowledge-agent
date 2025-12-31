import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideMarkdown } from 'ngx-markdown'
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideZard } from '@/shared/core/provider/providezard';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { authHttpInterceptorFn, provideAuth0 } from '@auth0/auth0-angular';
import { environment } from '../environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withFetch(), withInterceptors([authHttpInterceptorFn])),
    provideMarkdown(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideZard(),
    provideAuth0({
      domain: environment.AUTH0_DOMAIN,
      clientId: environment.AUTH0_CLIENT_ID,
      authorizationParams: {
        audience: environment.AUTH0_AUDIENCE,
        redirect_uri: typeof window !== 'undefined' ? window.location.origin : 'http://localhost:4200'
      },
      httpInterceptor: {
        allowedList: [
          {
            uri: `${environment.API_URL}/*`,
            tokenOptions: {
              authorizationParams: {
                audience: environment.AUTH0_AUDIENCE
              }
            }
          }
        ]
      }
    }),
  ]
};
