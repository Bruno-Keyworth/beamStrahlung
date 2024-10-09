{
  gStyle->SetOptStat(0);

  cerr << "hello1" << endl;

  const int nfile=1;

  TFile* f[nfile];
  f[0] = new TFile("/home/ilc/schwan/promotion/data/mag_field_map_det/graph_scan_field_perp_Y_z_0_400_IF1F.root");
  // f[0] = new TFile("/home/ilc/schwan/promotion/data/mag_field_map_det/graph_scan_field_perp_Y_z_0_600_IF1.root");
  // f[2] = new TFile("/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/ILD_l5_v03_field.root");
  // f[3] = new TFile("/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/ILD_l5_v05_field.root");
  // f[4] = new TFile("/home/ilc/jeans/lcgeo-1/ILD/ILD_l5_v11gamma.root");

  TH2F *x0[nfile];
  TH2F *bx[nfile];
  TH2F *by[nfile];
  TH2F *bz[nfile];
  for (int i = 0; i < nfile; i++)
  {

    cerr << i << " " << f[i] << endl;

    x0[i] = (TH2F *)f[i]->Get("Slice0/slice0_X0");
    x0[i]->SetMinimum(1e-6);
    bx[i] = (TH2F *)f[i]->Get("Slice0/slice0_Bx");
    by[i] = (TH2F *)f[i]->Get("Slice0/slice0_By");
    bz[i] = (TH2F *)f[i]->Get("Slice0/slice0_Bz");
  }

  x0[0]->SetTitle("ILD_FCCee_v01_fields");
  // x0[0]->SetTitle("ILD_FCCee_v01");
  // x0[2]->SetTitle("ILD_l5_v03");
  // x0[3]->SetTitle("ILD_l5_v05");
  // x0[4]->SetTitle("ILD_l5_v11gamma");

  TCanvas *cc = new TCanvas();

  TArrow *arr = new TArrow(0, 0, 2, 2, 0.005, ">");
  arr->SetLineColor(4);
  int iskip = 10;
  float scale = 2;
  for (int i = 0; i < nfile; i++)
  {
    cc->Clear();
    cc->SetLogz();
    x0[i]->Draw("col");
    for (int ix = 5; ix <= bx[i]->GetNbinsX(); ix += iskip)
    {
      for (int iy = 5; iy <= bx[i]->GetNbinsY(); iy += iskip)
      {
        float bbx = bx[i]->GetBinContent(ix, iy);
        float bbz = bz[i]->GetBinContent(ix, iy);
        float z = bx[i]->GetXaxis()->GetBinCenter(ix);
        float x = bx[i]->GetYaxis()->GetBinCenter(iy);
        arr->DrawArrow(z - scale * bbz, x - scale * bbx, z + scale * bbz, x + scale * bbx);
      }
    }
    cc->Print("2dfield" + TString(x0[i]->GetTitle()) + ".pdf");

    cc->Clear();
    cc->SetLogz();
    x0[i]->Draw("col");

    int ixStart = bx[i]->GetXaxis()->FindBin(0.0);
    int iyStart = bx[i]->GetYaxis()->FindBin(0.0);

    cerr << ixStart << " " << iyStart << endl;

    int xBinW = bx[i]->GetXaxis()->GetBinWidth(5);
    int xStep = 20;
    int yStep = 20;

    int nline = 1 + (bx[i]->GetNbinsY() - 10) / yStep;

    cerr << " ystep " << yStep << endl;

    int ix = ixStart;

    int iy = iyStart;

    for (int iline = 0; iline < nline; iline++)
    {

      int iy = iyStart + (iline - int(nline / 2)) * yStep;

      cerr << iline << " " << iy << " " << bx[i]->GetYaxis()->GetBinCenter(iy) << endl;

      for (int iposNeg = 1; iposNeg > -2; iposNeg -= 2)
      {

        float z = bx[i]->GetXaxis()->GetBinCenter(ix);
        float x = bx[i]->GetYaxis()->GetBinCenter(iy);

        while (fabs(z) < bx[i]->GetXaxis()->GetXmax())
        {

          int jx = bz[i]->GetXaxis()->FindBin(z);
          int jy = bz[i]->GetYaxis()->FindBin(x);

          float bbz = bz[i]->GetBinContent(jx, jy);
          float bbx = bx[i]->GetBinContent(jx, jy);

          //	  cout << jx << " " << jy << " " << z << " " << x << " " << bbz << " " << bbx << endl;

          float x0 = z;
          float x1 = z + iposNeg * xStep * xBinW;
          float y0 = x;
          float y1 = x + iposNeg * xStep * xBinW * bbx / bbz;

          if (y1 == y1 && x1 == x1 &&
              x1 >= bx[i]->GetXaxis()->GetXmin() && // x1<=bx[i]->GetXaxis()->GetXmax() &&
              x0 >= bx[i]->GetXaxis()->GetXmin()    //&& x0<=bx[i]->GetXaxis()->GetXmax()
          )
          {
            if (iposNeg > 0)
              arr->DrawArrow(x0, y0, x1, y1);
            else
              arr->DrawArrow(x1, y1, x0, y0);
          }

          z = x1;
          x = y1;
        }
      }
    }
    //
    //     //   for ( int ix=5; ix<=bx[i]->GetNbinsX(); ix+=iskip) {
    //     //   for ( int iy=5; iy<=bx[i]->GetNbinsY(); iy+=iskip) {
    //     // 	float bbx = bx[i]->GetBinContent( ix, iy );
    //     // 	float bbz = bz[i]->GetBinContent( ix, iy );
    //     // 	float z = bx[i]->GetXaxis()->GetBinCenter( ix );
    //     // 	float x = bx[i]->GetYaxis()->GetBinCenter( iy );
    //     // 	arr->DrawArrow(z-scale*bbz, x-scale*bbx, z+scale*bbz, x+scale*bbx);
    //     //   }
    //     // }
    //
    cc->Print("2dfieldB_" + TString(x0[i]->GetTitle()) + ".pdf");
    //
    //
  }
}
