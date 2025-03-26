import { Routes } from '@angular/router';
import { AuthGuard } from './auth.guard'; // Import the Auth Guard

// Importing all generated components
import { BlankComponent } from './pages/blank/blank.component';
import { ButtonsComponent } from './pages/buttons/buttons.component';
import { CardsComponent } from './pages/cards/cards.component';
import { ChartsComponent } from './pages/charts/charts.component';
import { ForgotPasswordComponent } from './pages/forgot-password/forgot-password.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { TablesComponent } from './pages/tables/tables.component';
import { UtilitiesAnimationComponent } from './pages/utilities-animation/utilities-animation.component';
import { UtilitiesBorderComponent } from './pages/utilities-border/utilities-border.component';
import { UtilitiesColorComponent } from './pages/utilities-color/utilities-color.component';
import { UtilitiesOtherComponent } from './pages/utilities-other/utilities-other.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: BlankComponent, canActivate: [AuthGuard] },  // Protected route
  { path: 'buttons', component: ButtonsComponent, canActivate: [AuthGuard] },
  { path: 'cards', component: CardsComponent, canActivate: [AuthGuard] },
  { path: 'charts', component: ChartsComponent, canActivate: [AuthGuard] },
  { path: 'forgotPassword', component: ForgotPasswordComponent },
  { path: 'register', component: RegisterComponent }, 
  { path: 'login', component: LoginComponent },
  { path: 'tables', component: TablesComponent, canActivate: [AuthGuard] },
  { path: 'utilities-animation', component: UtilitiesAnimationComponent, canActivate: [AuthGuard] },
  { path: 'utilities-border', component: UtilitiesBorderComponent, canActivate: [AuthGuard] },
  { path: 'utilities-color', component: UtilitiesColorComponent, canActivate: [AuthGuard] },
  { path: 'utilities-other', component: UtilitiesOtherComponent, canActivate: [AuthGuard] },

  { path: '**', component: NotFoundComponent }
];
