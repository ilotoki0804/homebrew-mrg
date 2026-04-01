class Mrg < Formula
  include Language::Python::Virtualenv

  desc "Clean miscellaneous files produced by macOS"
  homepage "https://github.com/ilotoki0804/mrg"
  url "https://files.pythonhosted.org/packages/source/m/mrg/mrg-0.1.0.post3.tar.gz"
  sha256 "06ac0852545e336c2ab11018cc7c762bf400476e1880a980543558302b74ce00"
  license "Apache-2.0"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    (testpath/"sample").mkpath
    (testpath/"sample"/".DS_Store").write("")

    output = shell_output("#{bin}/mrg #{testpath}/sample --ds-store --json")
    assert_match '"ds_store": 1', output
    assert_match '"ds_store_fixed": true', output
    refute_predicate testpath/"sample"/".DS_Store", :exist?
  end
end
